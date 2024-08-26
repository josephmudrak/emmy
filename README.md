# EMMY – Emotional Manager

## Requirements

- `portaudio`
- Tkinter is usually installed by default. If it is not, however, install `python3-tkinter` or equivalent.

## Additional Notes

- Installing the required PIP packages may fail with an error about insufficient storage space. This is because there are too many temporary files. To fix this, run the following command as root:

```sh
mount -o remount,size=5G /tmp
```

Increase `5G` as needed.
