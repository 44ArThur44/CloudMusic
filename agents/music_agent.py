import os
import shutil

class MusicAgent:
    def __init__(self, mode="guided", params=None, prompt=None):
        self.mode = mode
        self.params = params or {}
        self.prompt = prompt or ""
    
    def run(self):
        print(f"MOCK: Simulando geracao ({self.mode})")
        
        if self.mode == "guided" and self.params:
            print(f"  Tipo: {self.params.get('type', 'kick')}")
        
        # Garante pasta storage
        os.makedirs("storage", exist_ok=True)
        
        # Arquivo final (sempre o mesmo)
        target_file = "storage/music_001.wav"
        
        # Verifica se ja temos o arquivo mock
        if not os.path.exists(target_file):
            # Procura o original na raiz
            original = "music_001.wav"
            if os.path.exists(original):
                shutil.copy2(original, target_file)
                print(f"  Copiado {original} para storage")
            else:
                # Cria arquivo dummy se nao existir
                self._create_dummy_wav(target_file)
                print(f"  Criado arquivo dummy")
        
        print(f"MOCK OK: Retornando {target_file}")
        return target_file
    
    def _create_dummy_wav(self, filename):
        """Cria um arquivo WAV valido de 2 segundos"""
        import wave
        import struct
        
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(2)      # Estereo
            wav.setsampwidth(2)      # 16-bit
            wav.setframerate(44100)  # 44.1kHz
            
            # 2 segundos de silencio
            frames = struct.pack('<hh', 0, 0) * 44100 * 2
            wav.writeframes(frames)