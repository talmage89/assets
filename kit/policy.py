"""Delivery policy normalization, independent of Blender."""
import math


def density_bands(config, size):
    """Resolve limits to delivered pixels/m, preserving both legacy interfaces.

    New UV_DENSITY_BANDS declares reference_size. Older dictionaries without it
    already expressed delivered pixels/m. Legacy VERIFY_POLICY density_* fields
    scale from density_reference_size (2048 by default).
    """
    defaults=dict(p5_min=200,median_min=450,median_max=900,p95_max=1500)
    policy=config.get('VERIFY_POLICY',{})
    legacy={key:value for key,value in policy.items() if key.startswith('density_')}
    if 'UV_DENSITY_BANDS' in config:
        if legacy:
            raise ValueError('Declare density limits only in UV_DENSITY_BANDS')
        declared=config['UV_DENSITY_BANDS']
        reference=declared.get('reference_size',size)
        limits={key:declared[key] for key in defaults}
    else:
        reference=policy.get('density_reference_size',2048)
        limits={key:policy.get('density_'+key,value) for key,value in defaults.items()}
    if not math.isfinite(reference) or reference<=0 or size<=0:
        raise ValueError('Density reference and delivery sizes must be positive')
    result={key:value*size/reference for key,value in limits.items()}
    if not all(math.isfinite(value) and value>0 for value in result.values()):
        raise ValueError('Density limits must be finite and positive')
    if result['median_min']>=result['median_max']:
        raise ValueError('Density median_min must be below median_max')
    return result
