This MCP server uses the Youtube API to get a videos, video comments, channels, and playlists.

You can get an API key by going to Google Cloud Console, and creating a project that uses YouTube Data API v3

To connect it to Claude, you have to edit the claude_desktop_configuration.json file and add your server like this(Make sure to get the correct path to the parent folder!):

{
  "mcpServers": {
    "youtube": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\shriy\\mcpYoutube",
        "run",
        "mcpYoutube.py"
      ]
    }
  }
}

To test it out, try a prompt something like:
Can you find me good c++ pointer youtube videos using the comments?


