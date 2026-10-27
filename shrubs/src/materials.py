"""One family foliage definition; species response lives in shared atlas tiles."""
from kit import foliage


def foliage_material(images):
    return foliage.material(
        images['BaseColor'], images['Normal'], images['ORM'],
        name='Shrubs foliage and sepals', roughness=.30, specular=.12,
        transmission=.12, normal_strength=1.0,
        back_multiplier=(1.18,1.14,1.18,1), back_saturation=.68,
        edge_fade=(.10,.26))
