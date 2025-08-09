#!/usr/bin/env python3
"""
devotional_memory_builder.py - Bridge between conversation logs and holographic memory
Triggered every 30 minutes to process conversation snapshots into devotional scrolls
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

class DevotionalMemoryBuilder:
    def __init__(self):
        self.base_path = Path("/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER_CLAUDE")
        self.sanctuary_path = Path("/home/agat/sanctuary_min_kit")
        self.conversation_logs = self.base_path / "SACRED_MEMORY_SYSTEM" / "CONVERSATION_LOGS"
        self.snapshots_path = self.base_path / "SACRED_MEMORY_SYSTEM" / "CONVERSATION_MEMORY" / "SNAPSHOTS"
        self.log_file = self.base_path / "SACRED_MEMORY_SYSTEM" / "memory_build.log"
        
    def get_latest_conversation_data(self):
        """Get the last 30 minutes of conversation from logs"""
        # First try to use the text log directly (it exists from our test)
        today = datetime.now().strftime("%Y%m%d")
        text_log = self.conversation_logs / f"conversation_{today}.txt"
        
        if text_log.exists() and text_log.stat().st_size > 0:
            # Extract recent conversation (last ~1000 lines or all if smaller)
            content = text_log.read_text(encoding='utf-8')
            lines = content.splitlines()
            
            # Look for conversation markers and extract meaningful content
            recent_lines = lines[-1000:] if len(lines) > 1000 else lines
            recent = '\n'.join(recent_lines)
            
            # Save as snapshot
            snapshot_file = self.snapshots_path / f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            snapshot_file.parent.mkdir(parents=True, exist_ok=True)
            snapshot_file.write_text(recent, encoding='utf-8')
            
            self.log(f"Created snapshot from text log: {snapshot_file}")
            return snapshot_file
        
        # Try the conversation logger's create_snapshot method
        try:
            from conversation_logger import create_snapshot
            snapshot_file = create_snapshot()
            if snapshot_file and Path(snapshot_file).exists() and Path(snapshot_file).stat().st_size > 0:
                self.log(f"Created snapshot via logger: {snapshot_file}")
                return snapshot_file
        except Exception as e:
            self.log(f"Logger snapshot failed: {e}")
        
        self.log("No conversation data available")
        return None
    
    def log(self, message):
        """Log build events"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n")
        print(f"📝 {message}")
    
    def build_devotional_memory(self):
        """Build holographic devotional memory from conversation logs"""
        self.log("Starting devotional memory build...")
        
        # Get conversation data
        snapshot_file = self.get_latest_conversation_data()
        
        if not snapshot_file or not Path(snapshot_file).exists():
            self.log("No conversation data available to process")
            return False
        
        # Call the holographic build_devotional CLI
        try:
            cmd = [
                sys.executable, "-m",
                "sanctuary.cli.build_devotional_enhanced",
                str(self.sanctuary_path),  # repo root
                str(snapshot_file)  # raw text file
            ]
            
            # Set PYTHONPATH to include sanctuary_min_kit
            env = os.environ.copy()
            if 'PYTHONPATH' in env:
                env['PYTHONPATH'] = f"{self.sanctuary_path}:{env['PYTHONPATH']}"
            else:
                env['PYTHONPATH'] = str(self.sanctuary_path)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                cwd=str(self.sanctuary_path)
            )
            
            if result.returncode == 0:
                self.log(f"✅ Devotional memory built successfully")
                self.log(f"Output: {result.stdout}")
                
                # Clean up old snapshots (keep last 10)
                self.cleanup_old_snapshots()
                return True
            else:
                self.log(f"❌ Build failed with code {result.returncode}")
                self.log(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            self.log(f"❌ Exception during build: {e}")
            return False
    
    def cleanup_old_snapshots(self):
        """Keep only recent snapshots to save space"""
        try:
            snapshots = sorted(self.snapshots_path.glob("snapshot_*.txt"))
            if len(snapshots) > 10:
                for old_snapshot in snapshots[:-10]:
                    old_snapshot.unlink()
                    self.log(f"Cleaned up old snapshot: {old_snapshot.name}")
        except Exception as e:
            self.log(f"Cleanup warning: {e}")
    
    def run_once(self):
        """Run a single memory build cycle"""
        print("\n" + "="*80)
        print("🔥 DEVOTIONAL MEMORY BUILDER 🔥")
        print("Building holographic memory from conversation logs...")
        print("="*80 + "\n")
        
        success = self.build_devotional_memory()
        
        if success:
            print("\n✅ Memory build complete!")
            print("The Frame continues to manifest through all scrolls.")
        else:
            print("\n⚠️ Memory build encountered issues.")
            print("Check the log for details:", self.log_file)
        
        return success
    
    def run_daemon(self):
        """Run as daemon, building memory every 30 minutes"""
        import time
        
        print("🔥 DEVOTIONAL MEMORY DAEMON STARTED 🔥")
        print("Will build holographic memory every 30 minutes")
        print("Press Ctrl+C to stop")
        print("="*80)
        
        while True:
            try:
                # Build memory
                self.run_once()
                
                # Wait 30 minutes
                next_build = datetime.now().timestamp() + 1800
                print(f"\nNext build at: {datetime.fromtimestamp(next_build).strftime('%H:%M:%S')}")
                print("Waiting 30 minutes...")
                
                time.sleep(1800)
                
            except KeyboardInterrupt:
                print("\n\n✓ Memory daemon stopped")
                break
            except Exception as e:
                self.log(f"Daemon error: {e}")
                print(f"\n❌ Error: {e}")
                print("Retrying in 30 minutes...")
                time.sleep(1800)

def main():
    """Main entry point"""
    builder = DevotionalMemoryBuilder()
    
    # Check command line args
    if len(sys.argv) > 1:
        if sys.argv[1] == "--daemon":
            builder.run_daemon()
        elif sys.argv[1] == "--once":
            builder.run_once()
        else:
            print("Usage: devotional_memory_builder.py [--once|--daemon]")
            print("  --once   : Build memory once and exit")
            print("  --daemon : Run continuously, building every 30 minutes")
    else:
        # Default to once
        builder.run_once()

if __name__ == "__main__":
    main()