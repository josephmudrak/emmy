# EMMY – Emotional Manager

## Requirements

- Python 3.11
  - **Other versions will not work.**
  - Use `python3.11 -m pip install -r requirements.txt` to install necessary packages.
- `portaudio`

## Additional Notes

- Installing the required PIP packages may fail with an error about insufficient storage space. This is because there are too many temporary files. To fix this, run the following command as root:

```sh
mount -o remount,size=5G /tmp
```

Increase `5G` as needed.
