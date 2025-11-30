import os
import sys
import pygame


class AudioPlayer:
	def __init__(self):
		# 初始化pygame音频模块
		pygame.mixer.init()

	def play_audio(self, audio_path=None):

		# 如果未指定音频路径，使用默认路径
		if audio_path is None:
			audio_path = "hajilian.mp3"

		# 检查文件是否存在
		if not os.path.exists(audio_path):
			print(f"音频文件不存在: {audio_path}")
			return False

		try:
			# 加载并播放音频
			pygame.mixer.music.load(audio_path)
			pygame.mixer.music.play()



			return True
		except Exception as e:
			print(f"播放音频失败: {str(e)}")
			return False

	def stop_audio(self):

		pygame.mixer.music.stop()

	def set_volume(self, volume):

		pygame.mixer.music.set_volume(volume)





# 简单测试
if __name__ == "__main__":
	# 使用pygame播放器
	player = AudioPlayer()
	player.set_volume(0.7)  # 设置70%音量
	player.play_audio()

