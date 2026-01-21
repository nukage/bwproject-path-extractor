import os
import zipfile
import re
import sys
import argparse

def is_path_char(b):
    if 32 <= b <= 126:
        if chr(b) in '"<>|*?':
            return False
        return True
    if b > 127: return True
    return False

def extract_from_buffer(content, extensions):
    found = set()
    path_chars = set(range(32, 127)) - {ord('"'), ord('<'), ord('>'), ord('|'), ord('*'), ord('?')}
    
    # ASCII / UTF-8 search
    for ext in extensions:
        ext_b = b'.' + ext.encode('ascii')
        start = 0
        while True:
            idx = content.lower().find(ext_b, start)
            if idx == -1: break
            
            curr = idx - 1
            while curr >= 0:
                b = content[curr]
                if b in path_chars or b > 127:
                    curr -= 1
                else: break
            
            p_bytes = content[curr+1 : idx + len(ext_b)]
            if p_bytes:
                try:
                    p = p_bytes.decode('utf-8', errors='ignore').strip()
                    if '/' in p or '\\' in p or ':' in p:
                        win_match = re.search(r'[A-Za-z]:\\', p)
                        if win_match:
                            p = p[win_match.start():]
                        else:
                            while p and not (p[0].isalnum() or p[0] in ['/', '\\', '.', '_']):
                                p = p[1:]
                        
                        if p and len(p) > 4:
                            found.add(p)
                except: pass
            start = idx + 1

    # UTF-16LE search
    for ext in extensions:
        ext_u16 = ('.' + ext).encode('utf-16le')
        start = 0
        while True:
            idx = content.find(ext_u16, start)
            if idx == -1: break
            
            curr = idx - 2
            while curr >= 0:
                if curr + 1 < len(content) and content[curr+1] == 0:
                    if content[curr] in path_chars or content[curr] > 127:
                        curr -= 2
                        continue
                break
            
            p_bytes = content[curr+2 : idx + len(ext_u16)]
            if p_bytes:
                try:
                    p = p_bytes.decode('utf-16le', errors='ignore').strip()
                    if '/' in p or '\\' in p or ':' in p:
                        win_match = re.search(r'[A-Za-z]:\\', p)
                        if win_match:
                            p = p[win_match.start():]
                        else:
                            while p and not (p[0].isalnum() or p[0] in ['/', '\\', '.', '_']):
                                p = p[1:]
                        if p and len(p) > 4:
                            found.add(p)
                except: pass
            start = idx + 2
            
    return found

def main():
    parser = argparse.ArgumentParser(description="Extract sample paths from a Bitwig .bwproject file.")
    parser.add_argument("project_file", help="Path to the .bwproject file")
    parser.add_argument("-o", "--output", help="Output text file (default: extracted_paths.txt)", default="extracted_paths.txt")
    
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()
    target_file = args.project_file
    audio_exts = ['wav', 'mp3', 'flac', 'ogg', 'aif', 'aiff']
    all_paths = set()
    
    if not os.path.exists(target_file):
        print(f"Error: {target_file} not found.")
        return

    print(f"Scanning: {target_file}...")
    
    with open(target_file, "rb") as f:
        content = f.read()
    all_paths.update(extract_from_buffer(content, audio_exts))

    try:
        with zipfile.ZipFile(target_file, 'r') as z:
            for name in z.namelist():
                try:
                    with z.open(name) as member:
                        all_paths.update(extract_from_buffer(member.read(), audio_exts))
                except: continue
    except: pass

    with open(args.output, "w", encoding="utf-8") as f:
        for p in sorted(list(all_paths)):
            f.write(p + "\n")
            
    print(f"Done! Extracted {len(all_paths)} unique paths to {args.output}")

if __name__ == "__main__":
    main()
