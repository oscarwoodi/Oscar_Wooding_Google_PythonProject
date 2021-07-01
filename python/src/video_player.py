"""A video player class."""

from .video_library import VideoLibrary
from .command_parser import CommandParser
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video = None
        self._current_video_pause = None
        self.num_videos = len(self._video_library.get_all_videos())
        self.playlists = {}
        self.playlists_written = {}
        self.flaglist = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print('Here\'s a list of all available videos:')
        
        video_string = []
        for video in self._video_library.get_all_videos():
            tags_string = ' '.join(video.tags)
            video_string.append(f'{video.title} ({video.video_id}) [{tags_string}]')
    
        video_string.sort()

        for i in video_string:
            print(' ' + i)


    def play_video(self, video_id):
        """Plays the respective video.
        Args:
            video_id: The video_id to be played.
        """
        video_name = self._video_library.get_video(video_id)

        if video_name == None:
            print('Cannot play video: Video does not exist')
        elif self._current_video == None and video_id.strip().upper() not in self.flaglist:
            print(f'Playing video: {video_name.title}')
            self._current_video = video_name
        elif video_id.strip().upper() not in self.flaglist:
            print(f'Stopping video: {self._current_video.title}')
            print(f'Playing video: {video_name.title}')
            self._current_video = video_name
        else:
            print(f'Cannot play video: Video is currently flagged (reason: {self.flaglist[video_id.strip().upper()]})')


    def stop_video(self):
        """Stops the current video."""
        if self._current_video == None:
            print('Cannot stop video: No video is currently playing')
        else:
            print(f'Stopping video: {self._current_video.title}')
            self._current_video = None
            self._current_video_pause = None


    def play_random_video(self):
        """Plays a random video from the video library."""

        allowed_videos = []
        for video in self._video_library.get_all_videos():
            if video.video_id.strip().upper() not in self.flaglist:
                allowed_videos.append(video)
                

        if len(allowed_videos) < 1: 
            print('No videos available')
        elif self._current_video != None:
            print(f'Stopping video: {self._current_video.title}')

        rand_number = random.randint(0, len(allowed_videos) - 1)
        rand_videos = allowed_videos
        rand_video = rand_videos[rand_number]
        print(f'Playing video: {rand_video.title}')
        self._current_video = rand_video


    def pause_video(self):
        """Pauses the current video."""

        if self._current_video_pause != self._current_video and self._current_video != None :
            print(f'Pausing video: {self._current_video.title}')
            self._current_video_pause = self._current_video
        elif self._current_video == None:
            print('Cannot pause video: No video is currently playing')
        elif self._current_video_pause == self._current_video:
            print(f'Video already paused: {self._current_video_pause.title}')

    def continue_video(self):
        """Resumes playing the current video."""

        if self._current_video == None:
            print('Cannot continue video: No video is currently playing')
        elif self._current_video_pause == None:
            print('Cannot continue video: Video is not paused')
        else:
            print(f'Continuing video: {self._current_video.title}')
            self._current_video_pause = None

    def show_playing(self):
        """Displays video currently playing."""

        if self._current_video == None:
            print('No video is currently playing')
        elif self._current_video_pause == None:
            tags_string = ' '.join(self._current_video.tags)
            print(f'Currently playing: {self._current_video.title} ({self._current_video.video_id}) [{tags_string}]')
        else:
            tags_string = ' '.join(self._current_video.tags)
            print(f'Currently playing: {self._current_video.title} ({self._current_video.video_id}) [{tags_string}] - PAUSED')
            

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.strip().upper() in self.playlists:
            print('Cannot create playlist: A playlist with the same name already exists')
        else:
            self.playlists[playlist_name.strip().upper()] = []
            self.playlists_written[playlist_name] = []
            print(f'Successfully created new playlist: {playlist_name}')

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video_name = self._video_library.get_video(video_id)

        if playlist_name.strip().upper() not in self.playlists:
            print(f'Cannot add video to {playlist_name}: Playlist does not exist')
        else:
            songs = self.playlists[playlist_name.strip().upper()]
            
            if video_name == None:
                print(f'Cannot add video to {playlist_name}: Video does not exist')
            elif video_id.strip().upper() in songs and video_id.strip().upper() not in self.flaglist:
                print(f'Cannot add video to {playlist_name}: Video already added')
            elif video_id.strip().upper() not in self.flaglist:
                songs.append(video_id.strip().upper())
                self.playlists[playlist_name.strip().upper()] = songs
                print(f'Added video to {playlist_name}: {video_name.title}')
            else: 
                print(f'Cannot add video to {playlist_name}: Video is currently flagged (reason: {self.flaglist[video_id.strip().upper()]})')

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self.playlists) == 0:
            print('No playlists exist yet')
        else:
            print(f'Showing all playlists:')
         
            for playlist in sorted (self.playlists_written.keys()):
                print(f'    {playlist}')

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.strip().upper() not in self.playlists:
            print(f'Cannot show playlist {playlist_name}: Playlist does not exist')
        elif len(self.playlists[playlist_name.strip().upper()]) < 1:
            print(f'Showing playlist: {playlist_name}')
            print(' No videos here yet')
        else:
            print(f'Showing playlist: {playlist_name}')
            song_ids = self.playlists[playlist_name.strip().upper()]
            for id in song_ids:
                video_name = self._video_library.get_video(id.lower().strip())
                tags_string = ' '.join(video_name.tags)
                print(f'    {video_name.title} ({video_name.video_id}) [{tags_string}]')

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        video_name = self._video_library.get_video(video_id)

        if playlist_name.strip().upper() not in self.playlists:
            print(f'Cannot remove video from {playlist_name}: Playlist does not exist')
        else:
            songs = self.playlists[playlist_name.strip().upper()]
            if video_name == None:
                print(f'Cannot remove video from {playlist_name}: Video does not exist')
            elif video_id.strip().upper() not in songs:
                print(f'Cannot remove video from {playlist_name}: Video is not in playlist')
            else :
                songs.remove(video_id.strip().upper())
                self.playlists[playlist_name.strip().upper()] = songs
                print(f'Removed video from {playlist_name}: {video_name.title}')

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.strip().upper() not in self.playlists:
            print(f'Cannot clear playlist {playlist_name}: Playlist does not exist')
        else:
            self.playlists[playlist_name.strip().upper()] = []
            print(f'Successfully removed all videos from {playlist_name}')

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.strip().upper() not in self.playlists:
            print(f'Cannot delete playlist {playlist_name}: Playlist does not exist')
        else:
            self.playlists.pop(playlist_name.strip().upper())
            print(f'Deleted playlist: {playlist_name}')

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        search_term = search_term.lower()
        potential_videos = []
        potential_videos_id = []

        for video in self._video_library.get_all_videos():
            name = video.title
            tags_string = ' '.join(video.tags)
            
            if search_term in name.lower():
                    potential_videos.append(f'{name} ({video.video_id}) [{tags_string}]')
                    potential_videos_id.append(video.video_id)
        if len(potential_videos) == 0:
            print(f'No search results for {search_term}')
        else:
            print(f'Here are the results for {search_term}:')

            count = 1
            for term in sorted (potential_videos):
                print(f' {count}) {term}')
                count += 1

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it\'s a no.")
            answer = input()
        
            if answer.isdigit():
                answer = int(answer)

            potential_videos_id_sorted = sorted (potential_videos_id)

            parser = CommandParser(VideoPlayer())
        
            if answer in list(range(1, count)):
                answer_play = f'play {potential_videos_id_sorted[answer - 1]}'
                parser.execute_command(answer_play.split())
            
            else:
                None


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        video_tag = video_tag.lower()
        potential_videos = []
        potential_videos_id = []

        for video in self._video_library.get_all_videos():
            name = video.title
            tags_string = ' '.join(video.tags)
            
            if video_tag in tags_string.lower().split():
                    potential_videos.append(f'{name} ({video.video_id}) [{tags_string}]')
                    potential_videos_id.append(video.video_id)

        if len(potential_videos) == 0:
            print(f'No search results for {video_tag}')
        else:
            print(f'Here are the results for {video_tag}:')

            count = 1
            for term in sorted (potential_videos):
                print(f' {count}) {term}')
                count += 1

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it\'s a no.")
            answer = input()
        
            if answer.isdigit():
                answer = int(answer)

            potential_videos_id_sorted = sorted (potential_videos_id)

            parser = CommandParser(VideoPlayer())
        
            if answer in list(range(1, count)):
                answer_play = f'play {potential_videos_id_sorted[answer - 1]}'
                parser.execute_command(answer_play.split())
            
            else:
                None

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video_name = self._video_library.get_video(video_id)
        reason = flag_reason.strip()

        if video_name == None:
            print('Cannot flag video: Video does not exist')
        elif video_id.strip().upper() in self.flaglist:
            print('Cannot flag video: Video is already flagged')
        elif (reason) == "":
            self.flaglist[video_id.strip().upper()] = 'Not supplied'
            print(f'Successfully flagged video: {video_name.title} (reason: Not supplied)')
        else:
            self.flaglist[video_id.strip().upper()] = reason
            print(f'Successfully flagged video: {video_name.title} (reason: {reason})')

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
