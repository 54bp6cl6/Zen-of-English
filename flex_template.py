from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,
	SourceUser, SourceGroup, SourceRoom,
	TemplateSendMessage, ConfirmTemplate, MessageAction,
	ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
	PostbackAction, DatetimePickerAction,
	CameraAction, CameraRollAction, LocationAction,
	CarouselTemplate, CarouselColumn, PostbackEvent,CarouselContainer,
	StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
	ImageMessage, VideoMessage, AudioMessage, FileMessage,
	UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
	FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
	TextComponent, SpacerComponent, IconComponent, ButtonComponent,
	SeparatorComponent, QuickReply, QuickReplyButton,
	ImageSendMessage)
import json

def error(text):
	return TextSendMessage(text=text)

def single_button_message(message, button, background_color, button_clolor='#eedebe'):
	try:
		return FlexSendMessage(
			alt_text=message,
			contents=BubbleContainer(
				size='kilo',
				body=BoxComponent(
					layout='horizontal',
					background_color=background_color,
					contents=[
						BoxComponent(
							layout='horizontal',
							flex=3,
							contents=[
								TextComponent(text=message, size='md', gravity='center', wrap=True)
							]
						),
						BoxComponent(
							layout='horizontal',
							flex=2,
							contents=[
								ButtonComponent(
									style='secondary',
									color=button_clolor,
									height='sm',
									action=MessageAction(label=button, text=button)
								)
							]
						)
					]
				)
			)
		)
	except Exception as e:
		return flex.error(str('flex_template.py(single_button_message):{0}'.format(e)))

def multiple_choice(title, question, options, ans, theme, background_color='#b0daf2', button_clolor='#7cc1e9'):
	try:
		bubble = FlexSendMessage(
			alt_text="{0} : {1}".format(title,question), 
			contents=BubbleContainer(
				size='kilo',
				header=BoxComponent(
					layout='horizontal',
					background_color = background_color,
					padding_start='40%',
					padding_end='40%',
					contents=[
						BoxComponent(
							layout='horizontal',
							background_color=button_clolor,
							contents=[TextComponent(text=title, size='sm', align='center')])
					]),
				body=BoxComponent(
					layout='vertical',
					padding_top='0%',
					padding_bottom='0%',
					background_color = background_color,
					contents=[TextComponent(text=question, size='xl', align='center')]),
				footer=BoxComponent(layout='vertical', background_color=background_color, spacing='md', contents=[])))
		for option in options:
			data = {'theme': theme}
			data['situation'] = 'right' if option == ans else 'wrong'
			data_json = json.dumps(data)
			bubble.contents.footer.contents.append(
				ButtonComponent(style='secondary', color=button_clolor, action=PostbackAction(label=option, data=data_json)))
		return bubble
	except Exception as e:
		return flex.error(str('flex_template.py(multiple_choice):{0}'.format(e)))

def tf_test(title, key, value, ans, theme, background_color='#b0daf2', label_color='#7cc1e9', button_clolor='#2c9cdd'):
	try:
		bubble = FlexSendMessage(
			alt_text="{0} : {1}/{2}".format(title, key, value), 
			contents=BubbleContainer(
				size='kilo',
				header=BoxComponent(
					layout='horizontal',
					background_color = background_color,
					padding_start='40%',
					padding_end='40%',
					contents=[
						BoxComponent(
							layout='horizontal',
							background_color=label_color,
							contents=[TextComponent(text=title, size='sm', align='center')])]),
				body=BoxComponent(
					layout='vertical',
					background_color=background_color,
					padding_top='0%',
					spacing='xl',
					contents=[
						TextComponent(text=key, size='xl', align='center'),
						BoxComponent(
							layout='vertical',
							background_color = label_color,
							padding_top='5%',
							padding_bottom='5%',
							contents=[
								TextComponent(text=value, size='xl', align='center')])]),
				footer=BoxComponent(layout='horizontal', background_color=background_color, spacing='lg', contents=[])))
		for option in ['True', 'False']:
			data = {'theme': theme}
			data['situation'] = 'right' if option == str(ans) else 'wrong'
			data_json = json.dumps(data)
			bubble.contents.footer.contents.append(
				ButtonComponent(style='primary', color=button_clolor, action=PostbackAction(label=option, data=data_json)))
		return bubble
	except Exception as e:
		return flex.error(str('flex_template.py(tf_test):{0}'.format(e)))

def handwriting(title, description, question, ans, background_color='#b0daf2', label_color='#7cc1e9', button_clolor='#2c9cdd'):
	try:
		bubble = FlexSendMessage(
			alt_text="{0} : {1}".format(title, question), 
			contents=BubbleContainer(
				size='kilo',
				header=BoxComponent(
					layout='horizontal',
					background_color = background_color,
					padding_start='40%',
					padding_end='40%',
					contents=[
						BoxComponent(
							layout='horizontal',
							background_color=label_color,
							contents=[TextComponent(text=title, size='sm', align='center')])]),
				body=BoxComponent(
					layout='vertical',
					background_color=background_color,
					padding_top='0%',
					padding_bottonm='0%',
					spacing='xl',
					contents=[
						TextComponent(text=description, size='xl', align='center'),
						BoxComponent(
							layout='vertical',
							background_color = label_color,
							padding_top='5%',
							padding_bottom='5%',
							contents=[
								TextComponent(text=question, size='xl', align='center')])]),
				footer=BoxComponent(
					layout='horizontal',
					background_color = background_color,
					padding_start='70%',
					padding_top='0%',
					contents=[
						BoxComponent(
							layout='horizontal',
							contents=[
								ButtonComponent(
									style='secondary', color=background_color, height='sm',
									action=MessageAction(label='解答', text=ans))
							])])
				))
		return bubble
	except Exception as e:
		return flex.error(str('flex_template.py(handwriting):{0}'.format(e)))