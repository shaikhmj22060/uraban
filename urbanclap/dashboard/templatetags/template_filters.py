from django import template

register = template.Library()

@register.filter
def filter_by_category(subcategories, category_id):
    """Filter subcategories by category_id"""
    return [sub for sub in subcategories if sub.category.id == category_id]

@register.filter
def calculate_average(sub_count, cat_count):
    """Calculate average subcategories per category"""
    try:
        return round(sub_count / cat_count, 1) if cat_count > 0 else 0
    except (TypeError, ZeroDivisionError):
        return 0
@register.filter
@register.filter
def divide_by(value, arg):
    """Divide two values, handling QuerySets"""
    try:
        if hasattr(value, 'count'):  # If it's a QuerySet
            value = value.count()
        if hasattr(arg, 'count'):    # If it's a QuerySet
            arg = arg.count()
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0