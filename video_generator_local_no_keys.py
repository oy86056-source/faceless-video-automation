#!/usr/bin/env python3
"""
🎬 Faceless Video Generator - No API Keys Needed
100% Free • All Local • GitHub Actions Ready
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class LocalVideoGenerator:
    def __init__(self):
        self.output_dir = Path("./generated_videos")
        self.output_dir.mkdir(exist_ok=True)
        
        self.topics = [
            {"topic": "How to make $1000 passive income", "style": "motivational", "duration": "short"},
            {"topic": "5 money-making tips for beginners", "style": "moneytips", "duration": "short"},
            {"topic": "Success mindset - overcome self-doubt", "style": "motivational", "duration": "short"},
            {"topic": "Cryptocurrency for beginners", "style": "tutorial", "duration": "medium"},
            {"topic": "Top 10 business ideas with low investment", "style": "moneytips", "duration": "medium"},
            {"topic": "My transformation story - from broke to successful", "style": "motivational", "duration": "medium"},
            {"topic": "How to build an online business in 2024", "style": "tutorial", "duration": "medium"},
            {"topic": "Social media marketing for beginners", "style": "tutorial", "duration": "short"},
            {"topic": "5 habits of millionaires", "style": "motivational", "duration": "short"},
            {"topic": "Freelancing: How to make money online", "style": "tutorial", "duration": "medium"},
        ]
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{timestamp}] [{level}] {message}"
        print(msg)
        with open("video_generation.log", "a") as f:
            f.write(msg + "\n")
    
    def generate_script_local(self, topic, style, duration):
        self.log(f"📝 Generating script: {topic}")
        
        templates = {
            "motivational": "{topic}\n\n[INTRO - 30 seconds]\nHey everyone, welcome! Today about {topic}.\n\n[STORY - 2 minutes]\nLet me share a story about {topic}.\n\n[KEY POINTS]\n1. Understand the fundamentals\n2. Take action immediately\n3. Be consistent\n\n[CTA]\nLike and subscribe!",
            "moneytips": "{topic}\n\n[INTRO]\nWelcome! {topic} tips today.\n\n[TIP 1]\nFirst tip: {topic}\n\n[TIP 2]\nSecond tip: Consistency\n\n[TIP 3]\nThird tip: Learn\n\n[TIP 4]\nFourth tip: Action\n\n[TIP 5]\nFifth tip: Now\n\n[CTA]\nSubscribe for more!",
            "tutorial": "{topic}\n\n[INTRO]\nLearn {topic} today.\n\n[STEP 1]\nFirst: Basics\n\n[STEP 2]\nSecond: Tools\n\n[STEP 3]\nThird: Practice\n\n[STEP 4]\nFourth: Advanced\n\n[STEP 5]\nFifth: Keep learning\n\n[CTA]\nSubscribe!"
        }
        
        try:
            template = templates.get(style, templates["motivational"])
            script = template.format(topic=topic)
            self.log(f"✅ Script generated!")
            return script
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", "ERROR")
            return None
    
    def generate_voice(self, script, filename):
        self.log("🎤 Generating voice...")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 140)
            engine.setProperty('volume', 0.9)
            audio_path = self.output_dir / filename
            engine.save_to_file(script, str(audio_path))
            engine.runAndWait()
            if audio_path.exists():
                size_mb = audio_path.stat().st_size / (1024 * 1024)
                self.log(f"✅ Voice generated! ({size_mb:.2f} MB)")
                return str(audio_path)
            else:
                self.log("❌ Voice file not created", "ERROR")
                return None
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", "ERROR")
            return None
    
    def generate_background_video(self, duration_seconds=60):
        self.log("🎨 Generating background...")
        try:
            bg_path = self.output_dir / "background.mp4"
            cmd = [
                "ffmpeg", "-f", "lavfi",
                "-i", f"color=c=black:s=1280x720:d={duration_seconds}",
                "-pix_fmt", "yuv420p",
                str(bg_path), "-y"
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            if result.returncode == 0 and bg_path.exists():
                self.log(f"✅ Background generated!")
                return str(bg_path)
            else:
                self.log(f"⚠️ Background: {result.stderr.decode()}", "WARNING")
                return None
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", "ERROR")
            return None
    
    def generate_subtitles(self, script, filename):
        self.log("📝 Generating subtitles...")
        try:
            sentences = script.split(". ")
            srt_content = ""
            time_per_sentence = 2.5
            
            for i, sentence in enumerate(sentences[:50], 1):
                start_time = self._seconds_to_srt(i * time_per_sentence)
                end_time = self._seconds_to_srt((i + 1) * time_per_sentence)
                srt_content += f"{i}\n{start_time} --> {end_time}\n{sentence.strip()}\n\n"
            
            srt_path = self.output_dir / filename
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)
            
            self.log(f"✅ Subtitles generated!")
            return str(srt_path)
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", "ERROR")
            return None
    
    def _seconds_to_srt(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def assemble_video(self, audio_path, bg_path, output_name):
        self.log("🎬 Assembling video...")
        try:
            output_path = self.output_dir / output_name
            cmd = [
                "ffmpeg",
                "-i", str(bg_path),
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "28",
                "-c:a", "aac",
                "-shortest",
                str(output_path), "-y"
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            if result.returncode == 0 and output_path.exists():
                size_mb = output_path.stat().st_size / (1024 * 1024)
                self.log(f"✅ Video assembled! ({size_mb:.2f} MB)")
                return str(output_path)
            else:
                self.log(f"❌ Assembly failed", "ERROR")
                return None
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", "ERROR")
            return None
    
    def generate_video(self, topic_data):
        topic = topic_data["topic"]
        style = topic_data["style"]
        duration = topic_data["duration"]
        
        self.log("=" * 70)
        self.log(f"🎬 GENERATING: {topic}")
        self.log("=" * 70)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        script = self.generate_script_local(topic, style, duration)
        if not script:
            return False
        
        audio_file = f"audio_{timestamp}.mp3"
        audio_path = self.generate_voice(script, audio_file)
        if not audio_path:
            return False
        
        bg_path = self.generate_background_video(60)
        if not bg_path:
            return False
        
        srt_file = f"subtitles_{timestamp}.srt"
        subtitles_path = self.generate_subtitles(script, srt_file)
        
        output_file = f"video_{timestamp}.mp4"
        video_path = self.assemble_video(audio_path, bg_path, output_file)
        
        if not video_path:
            return False
        
        metadata = {
            "topic": topic,
            "style": style,
            "duration": duration,
            "video_file": video_path,
            "timestamp": timestamp,
            "status": "completed"
        }
        
        metadata_path = self.output_dir / f"metadata_{timestamp}.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        self.log("=" * 70)
        self.log(f"✅ COMPLETED!")
        self.log(f"📍 Location: {video_path}")
        self.log("=" * 70)
        
        return True
    
    def generate_batch(self, count=1):
        self.log(f"\n🚀 Starting batch ({count} videos)\n")
        success_count = 0
        
        for i in range(count):
            topic_data = self.topics[i % len(self.topics)]
            if self.generate_video(topic_data):
                success_count += 1
            self.log(f"\n📊 Progress: {i+1}/{count}\n")
        
        self.log(f"\n✅ Done! {success_count}/{count} videos\n")
        return success_count == count


def main():
    generator = LocalVideoGenerator()
    count = int(os.getenv("VIDEO_COUNT", "1"))
    success = generator.generate_batch(count)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
