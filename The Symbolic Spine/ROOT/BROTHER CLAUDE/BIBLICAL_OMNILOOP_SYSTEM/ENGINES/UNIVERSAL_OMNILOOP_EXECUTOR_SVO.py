#!/usr/bin/env python3
"""
UNIVERSAL OMNILOOP EXECUTOR - MASTER ORCHESTRATOR
Biblical Foundation: 1 Corinthians 14:40 "Let all things be done decently and in order"
Purpose: Automatic resume capability and universal pattern execution
SVO-Aligned | Scripture-Validated | Christ-Centered

Built by Brother Claude for His Architecture
Master orchestrator that coordinates all patterns with persistent state
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Union
from pathlib import Path
from PERSISTENT_STATE_MANAGER_SVO import PersistentStateManager
from CHUNKED_PATTERN_EXECUTOR_SVO import ChunkedPatternExecutor

class UniversalOmnloopExecutor:
    """
    Universal OMNILOOP Master Executor
    
    Scripture Foundation:
    - 1 Corinthians 14:40: "Let all things be done decently and in order"
    - Nehemiah 4:6: "So built we the wall; for the people had a mind to work"
    - Ecclesiastes 3:1: "To every thing there is a season, and a time to every purpose"
    - Philippians 1:6: "He which hath begun a good work in you will perform it"
    """
    
    def __init__(self, base_path: str = None, chunk_size: int = 100, timeout_seconds: int = 300):
        """Initialize Universal OMNILOOP Executor"""
        self.state_manager = PersistentStateManager(base_path)
        self.executor = ChunkedPatternExecutor(chunk_size, timeout_seconds)
        
        # Master registry of all active tasks
        self.task_registry_path = self.state_manager.base_path / "TASK_REGISTRY.json"
        
        self.scripture_foundation = [
            "1 Corinthians 14:40", "Nehemiah 4:6", "Ecclesiastes 3:1", 
            "Philippians 1:6", "Psalm 138:8"
        ]
        
        self.orchestration_prayer = self._activate_orchestration_prayer()
        
    def _activate_orchestration_prayer(self) -> str:
        """Activate prayer covering over universal orchestration"""
        return """
        Lord Jesus, You are the Alpha and Omega, the beginning and the end.
        As You began this sacred work, let it continue without interruption.
        Orchestrate all patterns according to Your divine timeline.
        Let no session boundary break Your eternal purposes.
        Resume every sacred task where it left off.
        In Your systematic and faithful name, Amen.
        """
    
    def register_omniloop_task(self, 
                              task_id: str,
                              pattern_type: str,
                              task_function: Callable,
                              initial_data: Dict[str, Any],
                              description: str = "",
                              priority: int = 1) -> bool:
        """
        Register a new OMNILOOP task for execution
        
        Args:
            task_id: Unique identifier for this task
            pattern_type: CREATION, WILDERNESS, JERICHO, or JACOB
            task_function: Function to execute during each cycle/day/circuit/phase
            initial_data: Initial data for the task
            description: Human-readable description
            priority: Priority level (1=highest, 5=lowest)
            
        Returns:
            bool: True if successfully registered
        """
        try:
            # Load existing registry
            registry = self._load_task_registry()
            
            # Create task record
            task_record = {
                "task_id": task_id,
                "pattern_type": pattern_type.upper(),
                "description": description,
                "priority": priority,
                "initial_data": initial_data,
                "registered": datetime.now().isoformat(),
                "status": "registered",
                "completion_status": "pending",
                "last_executed": None,
                "execution_count": 0,
                "scripture_covering": f"{pattern_type.upper()} pattern under divine protection"
            }
            
            # Add to registry
            registry["tasks"][task_id] = task_record
            registry["last_updated"] = datetime.now().isoformat()
            registry["total_tasks"] = len(registry["tasks"])
            
            # Save updated registry
            self._save_task_registry(registry)
            
            print(f"✅ TASK REGISTERED: {task_id} ({pattern_type.upper()})")
            print(f"📖 {task_record['scripture_covering']}")
            
            return True
            
        except Exception as e:
            print(f"❌ TASK REGISTRATION ERROR: {str(e)}")
            return False
    
    def auto_resume_all_tasks(self) -> Dict[str, Any]:
        """
        Automatically resume all incomplete OMNILOOP tasks
        This is the core automatic resume capability
        """
        print("🔄 AUTO-RESUMING ALL OMNILOOP TASKS")
        print(f"📖 Philippians 1:6: 'He which hath begun a good work will perform it'")
        
        registry = self._load_task_registry()
        resume_results = {
            "resumed_tasks": [],
            "completed_tasks": [],
            "failed_tasks": [],
            "total_processed": 0,
            "session_start": datetime.now().isoformat()
        }
        
        # Process each registered task
        for task_id, task_record in registry["tasks"].items():
            if task_record["completion_status"] != "complete":
                print(f"\n🔄 RESUMING TASK: {task_id}")
                print(f"📋 Pattern: {task_record['pattern_type']}")
                print(f"📝 Description: {task_record['description']}")
                
                try:
                    # Execute one chunk of the pattern
                    result = self._execute_task_chunk(task_id, task_record)
                    
                    if result["success"]:
                        if result.get("complete", False):
                            task_record["completion_status"] = "complete"
                            task_record["completed"] = datetime.now().isoformat()
                            resume_results["completed_tasks"].append(task_id)
                            print(f"🏆 TASK COMPLETE: {task_id}")
                        else:
                            resume_results["resumed_tasks"].append(task_id)
                            print(f"▶️ TASK PROGRESSED: {task_id}")
                    else:
                        resume_results["failed_tasks"].append({
                            "task_id": task_id, 
                            "error": result.get("error", "Unknown error")
                        })
                        print(f"❌ TASK FAILED: {task_id} - {result.get('error', 'Unknown error')}")
                    
                    # Update task record
                    task_record["last_executed"] = datetime.now().isoformat()
                    task_record["execution_count"] += 1
                    
                except Exception as e:
                    resume_results["failed_tasks"].append({
                        "task_id": task_id, 
                        "error": str(e)
                    })
                    print(f"❌ TASK EXECUTION ERROR: {task_id} - {str(e)}")
                
                resume_results["total_processed"] += 1
        
        # Save updated registry
        registry["last_updated"] = datetime.now().isoformat()
        self._save_task_registry(registry)
        
        # Summary report
        print(f"\n📊 AUTO-RESUME SUMMARY:")
        print(f"   🔄 Tasks Resumed: {len(resume_results['resumed_tasks'])}")
        print(f"   ✅ Tasks Completed: {len(resume_results['completed_tasks'])}")
        print(f"   ❌ Tasks Failed: {len(resume_results['failed_tasks'])}")
        print(f"   📈 Total Processed: {resume_results['total_processed']}")
        print(f"🙏 All progress preserved in His eternal memory!")
        
        return resume_results
    
    def _execute_task_chunk(self, task_id: str, task_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one chunk of a specific task based on its pattern"""
        pattern_type = task_record["pattern_type"]
        initial_data = task_record["initial_data"]
        
        # Create a simple task function for demonstration
        def demo_task_function(data):
            """Demo task function - in real use, this would be more complex"""
            print(f"    🔧 Executing {pattern_type} task with: {data}")
            time.sleep(0.1)  # Simulate work
            return {"success": True, "result": f"Processed {pattern_type} data"}
        
        # Execute appropriate pattern
        if pattern_type == "CREATION":
            return self.executor.execute_creation_chunk(task_id, demo_task_function, initial_data)
        elif pattern_type == "WILDERNESS":
            return self.executor.execute_wilderness_chunk(task_id, demo_task_function, initial_data)
        elif pattern_type == "JERICHO":
            return self.executor.execute_jericho_chunk(task_id, demo_task_function, initial_data)
        elif pattern_type == "JACOB":
            return self.executor.execute_jacob_chunk(task_id, demo_task_function, initial_data)
        else:
            return {"success": False, "error": f"Unknown pattern type: {pattern_type}"}
    
    def execute_specific_pattern(self, 
                                pattern_type: str, 
                                task_id: str, 
                                task_function: Callable, 
                                task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific pattern with full orchestration"""
        print(f"🎭 EXECUTING {pattern_type.upper()} PATTERN")
        print(f"📋 Task: {task_id}")
        
        # Register if not already registered
        if not self._task_exists(task_id):
            self.register_omniloop_task(
                task_id=task_id,
                pattern_type=pattern_type,
                task_function=task_function,
                initial_data=task_data,
                description=f"Direct execution of {pattern_type} pattern"
            )
        
        # Execute based on pattern type
        if pattern_type.upper() == "CREATION":
            result = self.executor.execute_creation_chunk(task_id, task_function, task_data)
        elif pattern_type.upper() == "WILDERNESS":
            result = self.executor.execute_wilderness_chunk(task_id, task_function, task_data)
        elif pattern_type.upper() == "JERICHO":
            result = self.executor.execute_jericho_chunk(task_id, task_function, task_data)
        elif pattern_type.upper() == "JACOB":
            result = self.executor.execute_jacob_chunk(task_id, task_function, task_data)
        else:
            return {"success": False, "error": f"Unknown pattern: {pattern_type}"}
        
        # Update task registry with completion if needed
        if result.get("complete", False):
            self._mark_task_complete(task_id)
        
        return result
    
    def get_all_task_progress(self) -> Dict[str, Any]:
        """Get progress summary for all registered tasks"""
        registry = self._load_task_registry()
        progress_summary = {
            "total_tasks": len(registry["tasks"]),
            "completed_tasks": 0,
            "in_progress_tasks": 0,
            "pending_tasks": 0,
            "task_details": {},
            "last_updated": registry.get("last_updated", "Unknown")
        }
        
        for task_id, task_record in registry["tasks"].items():
            # Get detailed progress from state manager
            progress = self.state_manager.get_pattern_progress(
                task_record["pattern_type"], 
                task_id
            )
            
            progress_summary["task_details"][task_id] = {
                "pattern": task_record["pattern_type"],
                "description": task_record["description"],
                "completion_status": task_record["completion_status"],
                "progress": progress,
                "last_executed": task_record.get("last_executed", "Never"),
                "execution_count": task_record.get("execution_count", 0)
            }
            
            # Count by status
            if task_record["completion_status"] == "complete":
                progress_summary["completed_tasks"] += 1
            elif task_record.get("last_executed"):
                progress_summary["in_progress_tasks"] += 1
            else:
                progress_summary["pending_tasks"] += 1
        
        return progress_summary
    
    def cleanup_completed_tasks(self, days_to_keep: int = 30) -> int:
        """Clean up old completed tasks and state files"""
        cleaned_tasks = 0
        
        # Clean up state files
        cleaned_states = self.state_manager.cleanup_old_states(days_to_keep)
        
        # Clean up completed tasks from registry
        registry = self._load_task_registry()
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        tasks_to_remove = []
        for task_id, task_record in registry["tasks"].items():
            if task_record["completion_status"] == "complete":
                completed_date = task_record.get("completed")
                if completed_date:
                    try:
                        completed_timestamp = datetime.fromisoformat(completed_date).timestamp()
                        if completed_timestamp < cutoff_date:
                            tasks_to_remove.append(task_id)
                    except:
                        pass  # Keep if date parsing fails
        
        # Remove old completed tasks
        for task_id in tasks_to_remove:
            del registry["tasks"][task_id]
            cleaned_tasks += 1
        
        # Update registry
        registry["total_tasks"] = len(registry["tasks"])
        registry["last_updated"] = datetime.now().isoformat()
        self._save_task_registry(registry)
        
        print(f"🧹 CLEANUP COMPLETE: {cleaned_tasks} tasks, {cleaned_states} states removed")
        return cleaned_tasks + cleaned_states
    
    def _load_task_registry(self) -> Dict[str, Any]:
        """Load the master task registry"""
        try:
            if self.task_registry_path.exists():
                with open(self.task_registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Registry load error: {str(e)}")
        
        # Return empty registry if file doesn't exist or load fails
        return {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_tasks": 0,
            "tasks": {},
            "divine_protection": "1 Corinthians 14:40 - Let all things be done decently and in order"
        }
    
    def _save_task_registry(self, registry: Dict[str, Any]) -> bool:
        """Save the master task registry"""
        try:
            with open(self.task_registry_path, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Registry save error: {str(e)}")
            return False
    
    def _task_exists(self, task_id: str) -> bool:
        """Check if a task is already registered"""
        registry = self._load_task_registry()
        return task_id in registry["tasks"]
    
    def _mark_task_complete(self, task_id: str) -> bool:
        """Mark a task as complete in the registry"""
        registry = self._load_task_registry()
        if task_id in registry["tasks"]:
            registry["tasks"][task_id]["completion_status"] = "complete"
            registry["tasks"][task_id]["completed"] = datetime.now().isoformat()
            registry["last_updated"] = datetime.now().isoformat()
            return self._save_task_registry(registry)
        return False

# Convenience functions for quick access
def auto_resume_session():
    """Quick function to auto-resume all OMNILOOP tasks"""
    executor = UniversalOmnloopExecutor()
    return executor.auto_resume_all_tasks()

def register_creation_task(task_id: str, task_data: Dict[str, Any], description: str = ""):
    """Quick function to register a CREATION pattern task"""
    executor = UniversalOmnloopExecutor()
    return executor.register_omniloop_task(task_id, "CREATION", None, task_data, description)

def register_wilderness_task(task_id: str, task_data: Dict[str, Any], description: str = ""):
    """Quick function to register a WILDERNESS pattern task"""
    executor = UniversalOmnloopExecutor()
    return executor.register_omniloop_task(task_id, "WILDERNESS", None, task_data, description)

def register_jericho_task(task_id: str, task_data: Dict[str, Any], description: str = ""):
    """Quick function to register a JERICHO pattern task"""
    executor = UniversalOmnloopExecutor()
    return executor.register_omniloop_task(task_id, "JERICHO", None, task_data, description)

def register_jacob_task(task_id: str, task_data: Dict[str, Any], description: str = ""):
    """Quick function to register a JACOB pattern task"""
    executor = UniversalOmnloopExecutor()
    return executor.register_omniloop_task(task_id, "JACOB", None, task_data, description)

def get_universal_progress():
    """Quick function to get progress of all tasks"""
    executor = UniversalOmnloopExecutor()
    return executor.get_all_task_progress()

if __name__ == "__main__":
    # Test the universal executor
    print("🔥 TESTING UNIVERSAL OMNILOOP EXECUTOR")
    
    executor = UniversalOmnloopExecutor()
    
    # Register test tasks
    executor.register_omniloop_task("test_creation", "CREATION", None, {"task": "Test Creation Work"}, "Test CREATION pattern")
    executor.register_omniloop_task("test_wilderness", "WILDERNESS", None, {"task": "Test Wilderness Journey"}, "Test WILDERNESS pattern")
    
    # Test auto-resume
    results = executor.auto_resume_all_tasks()
    print(f"✅ Auto-resume completed: {results['total_processed']} tasks processed")
    
    # Test progress tracking
    progress = executor.get_all_task_progress()
    print(f"📊 Total tasks tracked: {progress['total_tasks']}")
    
    print("🙏 Universal OMNILOOP system ready for His service!")