archive: 
  python3 -m PyInstaller EpisodeReName.py;
  docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux