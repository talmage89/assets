// Original far-wire example. UV.x = side 0/1; UV2.x = true diameter in metres.
// NORMAL carries the centreline tangent. MeshInstance transforms must have
// applied scale. Use the physical tube mesh nearby; disable shadow casting on
// these ribbons, and retain tube shadows. See README for the transition policy.
shader_type spatial;
render_mode unshaded, cull_disabled, skip_vertex_transform, depth_draw_never;

// Linear radiance colors, matching the Cycles inspection numeric inputs.
// Bare default; use (0.0015, 0.0017, 0.0015, 1) for jacketed routes.
// Deliberately no source_color hint: these values are already linear.
uniform vec4 wire_color = vec4(0.012, 0.013, 0.012, 1.0);
uniform float minimum_pixels = 0.85;
// Calibrated optical compensation; 1.0 is strict integrated coverage.
uniform float coverage_exponent = 0.55;
varying float coverage;
varying float half_width_pixels;
varying float support_width_pixels;

void vertex() {
    vec3 p = (MODELVIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;
    vec3 tangent_view = normalize((MODELVIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
    vec3 side = cross(tangent_view, normalize(-p));
    float side_length = length(side);
    side = side_length > 0.0001 ? side / side_length : vec3(1.0, 0.0, 0.0);
    float metres_per_pixel = 2.0 * max(0.01, -p.z) / (PROJECTION_MATRIX[1][1] * VIEWPORT_SIZE.y);
    float true_pixels = UV2.x / metres_per_pixel;
    float width_pixels = max(minimum_pixels, true_pixels);
    coverage = pow(min(1.0, true_pixels / width_pixels), coverage_exponent);
    half_width_pixels = width_pixels * 0.5;
    // Include the pixel filter's support outside the nominal band. Fading
    // inside the original quad alone would lose integrated wire coverage.
    support_width_pixels = width_pixels + 2.0;
    VERTEX = p + side * (UV.x - 0.5) * support_width_pixels * metres_per_pixel;
}

void fragment() {
    // Coverage compensation avoids turning distant wires into black ropes.
    float distance_pixels = (UV.x - 0.5) * support_width_pixels;
    float footprint = max(fwidth(distance_pixels), 0.0001);
    float left = max(-half_width_pixels, distance_pixels - footprint * 0.5);
    float right = min(half_width_pixels, distance_pixels + footprint * 0.5);
    float filtered_coverage = max(0.0, right - left) / footprint;
    ALBEDO = wire_color.rgb;
    ALPHA = filtered_coverage * coverage * wire_color.a;
}
