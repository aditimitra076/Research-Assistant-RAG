_ICON_PATHS = {
    "library": '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M4 4.5v17M8 6h8M8 10h8"/>',
    "folder": '<path d="M3 6.5A1.5 1.5 0 0 1 4.5 5H10l2 2h7.5A1.5 1.5 0 0 1 21 8.5v9a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 17.5z"/>',
    "file": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v5h5M9 12h6M9 16h6"/>',
    "search": '<circle cx="10.8" cy="10.8" r="6.3"/><path d="m15.5 15.5 4 4"/>',
    "upload": '<path d="M12 15V4m0 0L8 8m4-4 4 4"/><path d="M5 14v5h14v-5"/>',
    "message": '<path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5H5l1.2-3A7.5 7.5 0 1 1 20 11.5Z"/><path d="M8.5 11.5h7"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
    "trash": '<path d="M4 7h16M10 11v6m4-6v6M6 7l1 14h10l1-14M9 7V4h6v3"/>',
    "arrow-left": '<path d="m14 5-7 7 7 7M7 12h13"/>',
}


def icon_svg(name):
    paths = _ICON_PATHS[name]
    return (
        '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{paths}</svg>'
    )
