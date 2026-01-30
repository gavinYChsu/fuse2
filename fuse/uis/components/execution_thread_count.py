from typing import Optional
import gradio

import fuse.globals
from fuse import wording

EXECUTION_THREAD_COUNT_SLIDER : Optional[gradio.Slider] = None


def render() -> None:
	global EXECUTION_THREAD_COUNT_SLIDER

	EXECUTION_THREAD_COUNT_SLIDER = gradio.Slider(
		label = wording.get('execution_thread_count_slider_label'),
		value = fuse.globals.execution_thread_count,
		step = 1,
		minimum = 1,
		maximum = 128
	)


def listen() -> None:
	EXECUTION_THREAD_COUNT_SLIDER.change(update_execution_thread_count, inputs = EXECUTION_THREAD_COUNT_SLIDER)


def update_execution_thread_count(execution_thread_count : int = 1) -> None:
	fuse.globals.execution_thread_count = execution_thread_count

