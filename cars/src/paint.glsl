// Shared-texture factory paint. The GPU samples BaseColor with sRGB RGB decode;
// alpha remains linear. Presets and reference are embedded as GLB extras.
// No extra texture or material instance is needed per color.
vec3 factory_paint(vec4 base, vec3 tint, vec3 reference_tint) {
    return max(vec3(0.0), base.rgb + base.a * (tint - reference_tint));
}
float paint_coat_weight(float coverage) { return 0.10 + 0.90 * coverage; }
float paint_coat_roughness(float coverage) { return 0.385 - 0.35 * coverage; }
// Normal is OpenGL +Y; ORM is R=AO, G=roughness, B=metallic.
// Multiply ORM.b by the selected factory metallic uniform.

// Lamp surface: the same BaseColor alpha carries each emitter's calibrated
// power relative to 80. The selected lit state is an ordinary scalar uniform.
float lamp_emission_strength(float alpha, bool lit) { return lit ? 80.0 * alpha : 0.0; }
