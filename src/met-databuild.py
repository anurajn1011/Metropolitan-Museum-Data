import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Set
import os

class MetMuseumFetcher:
    """
    Fetches data from the Metropolitan Museum of Art API
    with session-based limits and resume capability.
    """
    
    BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"
    RATE_LIMIT = 20
    REQUEST_DELAY = 1.0 / RATE_LIMIT
    SUCCESS_LIMIT = 75  
    
    def __init__(self, base_output_dir: str = "met_data", department_id: int = None, department_name: str = None):
        self.base_output_dir = base_output_dir
        self.department_id = department_id
        
        # Create department-specific directory if department is specified
        if department_id and department_name:
            safe_name = "".join(c if c.isalnum() or c in (' ', '-') else '_' for c in department_name)
            safe_name = safe_name.replace(' ', '_')
            self.output_dir = os.path.join(base_output_dir, f"{department_id}_{safe_name}")
        else:
            self.output_dir = base_output_dir
        
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        
        self.objects_file = os.path.join(self.output_dir, "objects.jsonl")
        self.artists_file = os.path.join(self.output_dir, "artists.jsonl")
        self.departments_file = os.path.join(base_output_dir, "departments.jsonl")
        self.progress_file = os.path.join(self.output_dir, "progress.json")
        self.stats_file = os.path.join(self.output_dir, "fetch_stats.json")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.processed_objects = self._load_progress()
        self.processed_artists = set()
        
        if os.path.exists(self.artists_file):
            with open(self.artists_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        artist = json.loads(line)
                        self.processed_artists.add(artist.get("artist_name", ""))
                    except:
                        pass
        
        self.stats = {
            "session_attempted": 0,
            "session_successful": 0,
            "session_forbidden": 0,
            "total_processed": len(self.processed_objects),
            "start_time": datetime.now().isoformat()
        }
    
    def _load_progress(self) -> Set[int]:
        """Load list of already processed object IDs"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                return set(data.get("processed_objects", []))
        return set()
    
    def _save_progress(self):
        """Save progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump({
                "processed_objects": list(self.processed_objects),
                "last_updated": datetime.now().isoformat()
            }, f, indent=2)
    
    def _rate_limited_get(self, url: str, params: dict = None) -> Optional[dict]:
        """Make a rate-limited GET request"""
        time.sleep(self.REQUEST_DELAY)
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 403:
                return None
            
            if response.status_code == 429:
                print(f"Rate limited. Waiting 10 seconds...")
                time.sleep(10)
                return None
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return None
    
    def fetch_departments(self):
        """Fetch and save all departments"""
        print("Fetching departments...")
        url = f"{self.BASE_URL}/departments"
        data = self._rate_limited_get(url)
        
        os.makedirs(self.base_output_dir, exist_ok=True)
        
        if data and "departments" in data:
            with open(self.departments_file, 'w', encoding='utf-8') as f:
                for dept in data["departments"]:
                    department_record = {
                        "department_id": dept["departmentId"],
                        "displayName": dept["displayName"]
                    }
                    f.write(json.dumps(department_record) + '\n')
            print(f"Saved {len(data['departments'])} departments")
            return data["departments"]
        return []
    
    def fetch_object_ids_by_department(self, department_id: int) -> List[int]:
        """Fetch all object IDs for a specific department"""
        print(f"Fetching object IDs for department {department_id}...")
        url = f"{self.BASE_URL}/objects"
        params = {"departmentIds": department_id}
        
        data = self._rate_limited_get(url, params)
        
        if data and "objectIDs" in data:
            object_ids = data["objectIDs"]
            print(f"Found {len(object_ids)} total objects in department {department_id}")
            return object_ids
        return []
    
    def parse_artist_data(self, obj_data: dict) -> Optional[Dict]:
        """Extract artist information from object data"""
        if not obj_data.get("artistDisplayName"):
            return None
        
        artist_name = obj_data.get("artistDisplayName", "")
        artist_alpha = obj_data.get("artistAlphaSort", "")
        
        if not artist_name:
            return None
        
        def parse_year_to_timestamp(year_str):
            try:
                year = int(year_str)
                if year > 0:
                    return datetime(year, 1, 1).isoformat()
            except:
                pass
            return None
        
        begin_date = obj_data.get("artistBeginDate", "")
        end_date = obj_data.get("artistEndDate", "")
        
        artist_record = {
            "artist_name": artist_name,
            "artistAlphaSort": artist_alpha if artist_alpha else artist_name,
            "artistNationality": obj_data.get("artistNationality", ""),
            "artistBeginDate": parse_year_to_timestamp(begin_date),
            "artistEndDate": parse_year_to_timestamp(end_date)
        }
        
        return artist_record
    
    def parse_object_data(self, obj_data: dict, department_id: int) -> Dict:
        """Save all API data plus add department_id"""
        object_record = dict(obj_data)
        
        object_record["department_id"] = department_id
        
        if "objectID" in object_record and "object_id" not in object_record:
            object_record["object_id"] = object_record["objectID"]
        
        return object_record
    
    def _parse_dimension(self, measurements: List, dimension_type: str) -> Optional[float]:
        """Extract specific dimension from measurements array"""
        if not measurements:
            return None
        
        for measurement in measurements:
            if isinstance(measurement, dict):
                element_measurements = measurement.get("elementMeasurements", {})
                if dimension_type in element_measurements:
                    return element_measurements[dimension_type]
        return None
    
    def fetch_object_details(self, object_id: int, department_id: int) -> bool:
        """Fetch detailed information for a single object"""
        url = f"{self.BASE_URL}/objects/{object_id}"
        obj_data = self._rate_limited_get(url)
        
        self.stats["session_attempted"] += 1
        
        if not obj_data:
            self.stats["session_forbidden"] += 1
            return False
        
        try:
            # Save object data
            object_record = self.parse_object_data(obj_data, department_id)
            with open(self.objects_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(object_record) + '\n')
            
            # Save artist data if exists
            artist_record = self.parse_artist_data(obj_data)
            if artist_record:
                artist_key = artist_record["artist_name"]
                if artist_key not in self.processed_artists:
                    with open(self.artists_file, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(artist_record) + '\n')
                    self.processed_artists.add(artist_key)
            
            self.stats["session_successful"] += 1
            return True
            
        except Exception as e:
            print(f"Error processing object {object_id}: {e}")
            return False
    
    def save_stats(self):
        """Save statistics to file"""
        self.stats["end_time"] = datetime.now().isoformat()
        self.stats["total_processed"] = len(self.processed_objects)
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2)
    
    def fetch_department_data(self, department_id: int, auto_continue: bool = False, session_delay: int = 60):
        """
        Fetch data for a specific department (session-limited)
        
        Args:
            department_id: The department ID to fetch
            auto_continue: If True, automatically continues until all data is fetched
            session_delay: Seconds to wait between sessions (default 60)
        """
        print(f"\n{'='*70}")
        print(f"Starting data collection for department {department_id}")
        print(f"Session limit: {self.SUCCESS_LIMIT} successful objects per run")
        if auto_continue:
            print(f"Delay between sessions: {session_delay} seconds")
        print(f"{'='*70}\n")
        
        # Fetch object IDs
        object_ids = self.fetch_object_ids_by_department(department_id)
        
        if not object_ids:
            print("No objects found!")
            return
        
        session_number = 1
        
        while True:
            # Filter out already processed objects
            remaining_ids = [oid for oid in object_ids if oid not in self.processed_objects]
            
            if session_number == 1:
                print(f"Total objects: {len(object_ids)}")
                print(f"Already processed: {len(self.processed_objects)}")
                print(f"Remaining: {len(remaining_ids)}")
            
            if not remaining_ids:
                print("\n All objects already processed!")
                break
            
            print(f"\n{'='*70}")
            print(f"SESSION {session_number}")
            print(f"{'='*70}")
            print(f"Fetching up to {self.SUCCESS_LIMIT} objects this session...")
            print(f"Remaining to process: {len(remaining_ids)}\n")
            
            # Reset session stats
            self.stats["session_attempted"] = 0
            self.stats["session_successful"] = 0
            self.stats["session_forbidden"] = 0
            self.stats["start_time"] = datetime.now().isoformat()
            
            successful_this_session = 0
            
            for i, obj_id in enumerate(remaining_ids, 1):
                # Check if we've hit the success limit
                if successful_this_session >= self.SUCCESS_LIMIT:
                    print(f"\n✓ Reached session limit ({self.SUCCESS_LIMIT} successful fetches)")
                    break
                
                success = self.fetch_object_details(obj_id, department_id)
                
                if success:
                    successful_this_session += 1
                    self.processed_objects.add(obj_id)
                    
                    # Save progress periodically
                    if successful_this_session % 25 == 0:
                        self._save_progress()
                else:
                    # Still mark as processed to avoid retrying 403s
                    self.processed_objects.add(obj_id)
                
                # Progress update
                if i % 50 == 0 or (successful_this_session > 0 and successful_this_session % 25 == 0):
                    print(f"Checked: {i} | "
                          f"Session Success: {successful_this_session}/{self.SUCCESS_LIMIT} | "
                          f"Session 403s: {self.stats['session_forbidden']}")
            
            # Save final progress and stats
            self._save_progress()
            self.save_stats()
            
            # Show session summary
            print(f"\n{'='*70}")
            print(f"Session {session_number} Complete!")
            print(f"{'='*70}")
            print(f"  Successful: {self.stats['session_successful']}")
            print(f"  Restricted: {self.stats['session_forbidden']}")
            print(f"\nOverall Progress:")
            print(f"  Total objects: {len(object_ids)}")
            print(f"  Completed: {len(self.processed_objects)} ({len(self.processed_objects)/len(object_ids)*100:.1f}%)")
            print(f"  Remaining: {len(object_ids) - len(self.processed_objects)}")
            
            # Check if we should continue
            remaining_after = len(object_ids) - len(self.processed_objects)
            
            if remaining_after == 0:
                print(f"\n All objects fetched!")
                print(f"{'='*70}\n")
                break
            
            if not auto_continue:
                runs_needed = remaining_after // self.SUCCESS_LIMIT + 1
                print(f"\n💡 Run this script {runs_needed} more times to fetch all data")
                print(f"{'='*70}\n")
                break
            
            session_number += 1
            print(f"\n Waiting {session_delay} seconds before next session...")
            print(f"   (This gives the API time to reset)")
            print(f"   Press Ctrl+C to stop\n")
            
            try:
                time.sleep(session_delay)
            except KeyboardInterrupt:
                print(f"\n\n⚠️  Stopped by user. Progress has been saved.")
                print(f"   Run again to continue from where you left off.")
                print(f"{'='*70}\n")
                break


def get_department_name(departments: List[Dict], department_id: int) -> str:
    """Get department name by ID"""
    for dept in departments:
        dept_id = dept.get("departmentId") or dept.get("department_id")
        if dept_id == department_id:
            return dept.get("displayName") or dept.get("name", f"Department_{department_id}")
    return f"Department_{department_id}"


def load_departments(base_dir: str = "met_data") -> List[Dict]:
    """Load departments from file"""
    departments_file = os.path.join(base_dir, "departments.jsonl")
    departments = []
    
    if os.path.exists(departments_file):
        with open(departments_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    dept = json.loads(line)
                    # Normalize keys
                    normalized = {
                        "departmentId": dept.get("department_id") or dept.get("departmentId"),
                        "displayName": dept.get("displayName") or dept.get("name", "")
                    }
                    departments.append(normalized)
                except:
                    pass
    
    return departments


def main():
    """Main execution function"""
    import sys
    
    auto_mode = '--auto' in sys.argv or '-a' in sys.argv
    department_id = None
    session_delay = 60  
    
    for arg in sys.argv[1:]:
        if arg.isdigit():
            department_id = int(arg)
        elif arg.startswith('--delay='):
            try:
                session_delay = int(arg.split('=')[1])
            except:
                pass
    
    # Base directory
    base_dir = "met_data"
    
    # Fetch or load departments list
    departments_file = os.path.join(base_dir, "departments.jsonl")
    
    if not os.path.exists(departments_file):
        print("Fetching departments list...")
        temp_fetcher = MetMuseumFetcher(base_output_dir=base_dir)
        departments = temp_fetcher.fetch_departments()
    else:
        departments = load_departments(base_dir)
    
    
    # Get department name
    department_name = get_department_name(departments, department_id)
    
    # Check if department exists
    if not any(d['departmentId'] == department_id for d in departments):
        print(f"\n Error: Department {department_id} not found!")
        print("\nAvailable departments:")
        for dept in departments:
            print(f"  {dept['departmentId']:2d}: {dept['displayName']}")
        return
    
    print(f"\n{'='*70}")
    print(f"Department: {department_name} (ID: {department_id})")
    print(f"Data will be saved to: {base_dir}/{department_id}_{department_name.replace(' ', '_')}/")
    print(f"{'='*70}")
    
    # Create fetcher with department-specific directory
    fetcher = MetMuseumFetcher(
        base_output_dir=base_dir,
        department_id=department_id,
        department_name=department_name
    )
    
    # Fetch data for the specified department
    fetcher.fetch_department_data(
        department_id=department_id,
        auto_continue=auto_mode,
        session_delay=session_delay
    )


if __name__ == "__main__":
    main()