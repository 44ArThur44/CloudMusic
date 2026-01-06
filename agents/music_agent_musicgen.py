import replicate
import os
import requests
import uuid
import time

class MusicAgent:
    def __init__(self, mode="guided", params=None, prompt=None):
        self.mode = mode
        self.params = params or {}
        self.prompt = prompt or ""
        
    def _extract_duration_from_prompt(self, prompt):
        """Extrai duração do prompt (ex: '... 4 seconds' ou '... 4s')"""
        import re
        
        # Procura padrões como "4 seconds", "10s", "15 sec"
        patterns = [
            r'(\d+)\s*seconds?',
            r'(\d+)s\b',
            r'(\d+)\s*sec\b',
            r'duration\s*:\s*(\d+)',
            r'length\s*:\s*(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                duration = int(match.group(1))
                # Limitar a máximo 30s da API
                return min(duration, 30)
        
        return None  # Não encontrou duração no prompt
    
    def _build_prompt_from_params(self):
        type_map = {
            "kick": "kick drum loop, punchy",
            "bass": "bassline, sub frequencies",
            "texture": "atmospheric texture, pads",
            "riser": "riser effect, building tension"
        }
        
        base = type_map.get(self.params.get("type", "kick"), "electronic loop")
        
        bpm = self.params.get("bpm", 128)
        base += f", {bpm} BPM"
        
        intensity = self.params.get("intensity", 3)
        intensity_map = {1: "very soft", 2: "soft", 3: "medium", 4: "intense", 5: "very intense"}
        base += f", {intensity_map.get(intensity, 'medium')}"
        
        if self.params.get("dark"):
            base += ", dark mood"
        if self.params.get("ambient"):
            base += ", ambient atmosphere"
        if self.params.get("energetic"):
            base += ", energetic"
            
        return base
    
    def run(self):
        # CÓDIGO APENAS PARA API REAL
        print(f"API REAL: Generating with Replicate ({self.mode} mode)...")
        os.makedirs("storage", exist_ok=True)
        
        if self.mode == "guided":
            final_prompt = self._build_prompt_from_params()
            # No modo guided, SEMPRE usa os params
            duration = self.params.get("duration", 5)
            print(f"Guided mode - Duration from params: {duration}s")
        else:
            # Modo advanced
            final_prompt = self.prompt
            print(f"Advanced mode - Prompt: {final_prompt}")
            
            # 1. Primeiro tenta extrair do prompt
            extracted = self._extract_duration_from_prompt(self.prompt)
            
            # 2. Se não extraiu do prompt, tenta params
            if extracted is not None:
                duration = extracted
                print(f"Extracted duration from prompt: {duration}s")
            else:
                duration = self.params.get("duration", 5)
                print(f"Duration from params: {duration}s")
        
        # Limite da API (30 segundos máximo)
        max_duration = 30
        final_duration = min(duration, max_duration)
        print(f"Final duration to use: {final_duration}s")
        
        try:
            output = replicate.run(
                "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
                input={
                    "prompt": final_prompt,
                    "duration": final_duration,
                    "model_version": "stereo-melody-large",
                    "temperature": 1.0,
                    "top_k": 250,
                    "top_p": 0.8
                }
            )
            
            audio_url = output
            print(f"Audio generated on Replicate")
            
            unique_id = str(uuid.uuid4())[:8]
            filename = f"storage/music_api_{self.mode}_{unique_id}.wav"
            
            response = requests.get(audio_url, timeout=30)
            response.raise_for_status()
            
            with open(filename, "wb") as f:
                f.write(response.content)
                
            print(f"Saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"API ERROR: {e}")
            fallback = "music_001.wav" if os.path.exists("music_001.wav") else None
            if fallback:
                import shutil
                fallback_path = f"storage/fallback_{int(time.time())}.wav"
                shutil.copy2(fallback, fallback_path)
                return fallback_path
            raise