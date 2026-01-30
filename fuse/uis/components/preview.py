from typing import Any, Dict, List, Optional
import cv2
import gradio

import fuse.globals
from fuse import wording
from fuse.typing import Frame, Face
from fuse.vision import get_video_frame, count_video_frame_total, normalize_frame_color, resize_frame_dimension, read_static_image
from fuse.face_analyser import get_one_face
from fuse.face_reference import get_face_reference, set_face_reference
from fuse.predictor import predict_frame
from fuse.processors.frame.core import load_frame_processor_module
from fuse.utilities import is_video, is_image
from fuse.uis.typing import ComponentName
from fuse.uis.core import get_ui_component, register_ui_component

PREVIEW_IMAGE : Optional[gradio.Image] = None
PREVIEW_FRAME_SLIDER : Optional[gradio.Slider] = None


def render() -> None:
	global PREVIEW_IMAGE
	global PREVIEW_FRAME_SLIDER

	preview_image_args: Dict[str, Any] =\
	{
		'label': wording.get('preview_image_label'),
		'interactive': False
	}
	preview_frame_slider_args: Dict[str, Any] =\
	{
		'label': wording.get('preview_frame_slider_label'),
		'step': 1,
		'minimum': 0,
		'maximum': 100,
		'visible': False
	}
	conditional_set_face_reference()
	source_face = get_one_face(read_static_image(fuse.globals.source_path))
	reference_face = get_face_reference() if 'reference' in fuse.globals.face_recognition else None
	if is_image(fuse.globals.target_path):
		target_frame = read_static_image(fuse.globals.target_path)
		preview_frame = process_preview_frame(source_face, reference_face, target_frame)
		preview_image_args['value'] = normalize_frame_color(preview_frame)
	if is_video(fuse.globals.target_path):
		temp_frame = get_video_frame(fuse.globals.target_path, fuse.globals.reference_frame_number)
		preview_frame = process_preview_frame(source_face, reference_face, temp_frame)
		preview_image_args['value'] = normalize_frame_color(preview_frame)
		preview_image_args['visible'] = True
		preview_frame_slider_args['value'] = fuse.globals.reference_frame_number
		preview_frame_slider_args['maximum'] = count_video_frame_total(fuse.globals.target_path)
		preview_frame_slider_args['visible'] = True
	PREVIEW_IMAGE = gradio.Image(**preview_image_args)
	PREVIEW_FRAME_SLIDER = gradio.Slider(**preview_frame_slider_args)
	register_ui_component('preview_frame_slider', PREVIEW_FRAME_SLIDER)


def listen() -> None:
	PREVIEW_FRAME_SLIDER.change(update_preview_image, inputs = PREVIEW_FRAME_SLIDER, outputs = PREVIEW_IMAGE)
	multi_component_names : List[ComponentName] =\
	[
		'source_image',
		'target_image',
		'target_video'
	]
	for component_name in multi_component_names:
		component = get_ui_component(component_name)
		if component:
			for method in [ 'upload', 'change', 'clear' ]:
				getattr(component, method)(update_preview_image, inputs = PREVIEW_FRAME_SLIDER, outputs = PREVIEW_IMAGE)
				getattr(component, method)(update_preview_frame_slider, inputs = PREVIEW_FRAME_SLIDER, outputs = PREVIEW_FRAME_SLIDER)
	update_component_names : List[ComponentName] =\
	[
		'face_recognition_dropdown',
		'frame_processors_checkbox_group',
		'face_swapper_model_dropdown',
		'face_enhancer_model_dropdown',
		'frame_enhancer_model_dropdown'
	]
	for component_name in update_component_names:
		component = get_ui_component(component_name)
		if component:
			component.change(update_preview_image, inputs = PREVIEW_FRAME_SLIDER, outputs = PREVIEW_IMAGE)
	select_component_names : List[ComponentName] =\
	[
		'reference_face_position_gallery',
		'face_analyser_direction_dropdown',
		'face_analyser_age_dropdown',
		'face_analyser_gender_dropdown'
	]
	for component_name in select_component_names:
		component = get_ui_component(component_name)
		if component:
			component.select(update_preview_image, inputs = PREVIEW_FRAME_SLIDER, outputs = PREVIEW_IMAGE)
	change_component_names : List[ComponentName] =\
	[
		'reference_face_distance_slider',
		'face_enhancer_blend_slider',
		'frame_enhancer_blend_slider'
	]
	for component_name in change_component_names:
		component = get_ui_component(component_name)
		if component:
			component.change(update_preview_image, inputs = PREVIEW_FRAME_SLIDER, outputs = PREVIEW_IMAGE)


def update_preview_image(frame_number : int = 0) -> gradio.Image:
	conditional_set_face_reference()
	source_face = get_one_face(read_static_image(fuse.globals.source_path))
	reference_face = get_face_reference() if 'reference' in fuse.globals.face_recognition else None
	if is_image(fuse.globals.target_path):
		target_frame = read_static_image(fuse.globals.target_path)
		preview_frame = process_preview_frame(source_face, reference_face, target_frame)
		preview_frame = normalize_frame_color(preview_frame)
		return gradio.Image(value = preview_frame)
	if is_video(fuse.globals.target_path):
		fuse.globals.reference_frame_number = frame_number
		temp_frame = get_video_frame(fuse.globals.target_path, fuse.globals.reference_frame_number)
		preview_frame = process_preview_frame(source_face, reference_face, temp_frame)
		preview_frame = normalize_frame_color(preview_frame)
		return gradio.Image(value = preview_frame)
	return gradio.Image(value = None)


def update_preview_frame_slider(frame_number : int = 0) -> gradio.Slider:
	if is_image(fuse.globals.target_path):
		return gradio.Slider(value = None, maximum = None, visible = False)
	if is_video(fuse.globals.target_path):
		fuse.globals.reference_frame_number = frame_number
		video_frame_total = count_video_frame_total(fuse.globals.target_path)
		return gradio.Slider(maximum = video_frame_total, visible = True)
	return gradio.Slider()


def process_preview_frame(source_face : Face, reference_face : Face, temp_frame : Frame) -> Frame:
	temp_frame = resize_frame_dimension(temp_frame, 640, 640)
	if predict_frame(temp_frame):
		return cv2.GaussianBlur(temp_frame, (99, 99), 0)
	for frame_processor in fuse.globals.frame_processors:
		frame_processor_module = load_frame_processor_module(frame_processor)
		if frame_processor_module.pre_process('preview'):
			temp_frame = frame_processor_module.process_frame(
				source_face,
				reference_face,
				temp_frame
			)
	return temp_frame


def conditional_set_face_reference() -> None:
	if 'reference' in fuse.globals.face_recognition and not get_face_reference():
		reference_frame = get_video_frame(fuse.globals.target_path, fuse.globals.reference_frame_number)
		reference_face = get_one_face(reference_frame, fuse.globals.reference_face_position)
		set_face_reference(reference_face)
