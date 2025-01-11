"""
Central control module for managing different news channels.
"""
from typing import Optional, Dict, Any

from .news_channels import (
    straight_times,
    new_york_times,
    cna,
)
from .news_channels.news_config import NEWS_CHANNELS

class NewsChannelNotFoundError(Exception):
    """Raised when specified news channel is not found."""
    pass

class NewsController:
    _channel_modules = {
        "straight_times": straight_times,
        "new_york_times": new_york_times,
        "cna": cna,
    }

    @classmethod
    def _get_channel_module(cls, channel_name: str):
        """Get the module for the specified channel name."""
        if channel_name not in cls._channel_modules:
            raise NewsChannelNotFoundError(f"News channel '{channel_name}' not found")
        return cls._channel_modules[channel_name]

    @classmethod
    async def update_news(cls, channel_name: str) -> None:
        """
        Update news for the specified channel.
        
        Args:
            channel_name: Name of the news channel to update
            
        Raises:
            NewsChannelNotFoundError: If the specified channel is not found
        """
        channel_module = cls._get_channel_module(channel_name)
        await channel_module.update_news()

    @classmethod
    async def get_news(cls, channel_name: str) -> Dict[str, Any]:
        """
        Get news from the specified channel.
        
        Args:
            channel_name: Name of the news channel to get news from
            
        Returns:
            Dict containing news data
            
        Raises:
            NewsChannelNotFoundError: If the specified channel is not found
        """
        channel_module = cls._get_channel_module(channel_name)
        return await channel_module.get_news()

    @classmethod
    def get_available_channels(cls) -> Dict[str, Dict[str, str]]:
        """
        Get list of all available news channels and their configurations.
        
        Returns:
            Dict containing channel configurations
        """
        return NEWS_CHANNELS

if __name__ == "__main__":
    import asyncio
    
    async def main():
        try:
            # Print available channels
            print("Available News Channels:")
            channels = NewsController.get_available_channels()
            for channel_id, channel_info in channels.items():
                print(f"- {channel_info['name']} (ID: {channel_id})")
            
            print("\nTesting news operations for each channel:")
            # for channel_id in channels.keys():
            #     print(f"\nTesting {channel_id}:")
            #     print("1. Updating news...")
            #     await NewsController.update_news(channel_id)
            #     print("2. Getting news...")
            #     news = await NewsController.get_news(channel_id)
            #     print(f"News received: {news}")
                
            # Test error handling with invalid channel
            print("\nTesting error handling:")
            await NewsController.get_news("invalid_channel")
            
        except NewsChannelNotFoundError as e:
            print(f"Error caught successfully: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # Run the async main function
    asyncio.run(main())


    # To run this file as a script:
    # python -m app.news_control 