from neighborlink.comments.models import CommentWithRating
from neighborlink.comments.forms import CommentFormWithRating

def get_model():
	return CommentWithRating

def get_form():
	return CommentFormWithRating	