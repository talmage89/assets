// Original far-wire example. UV.x = side 0/1; UV2.x = true diameter in metres.
// NORMAL carries the centreline tangent. MeshInstance transforms must have
// applied scale. Use the physical tube mesh nearby; disable shadow casting on
// these ribbons, and retain tube shadows. See README for the transition policy.
shader_type spatial;
render_mode unshaded, cull_disabled, skip_vertex_transform, depth_draw_never;

uniform vec4 wire_color : source_color = vec4(0.025, 0.028, 0.030, 1.0);
uniform float minimum_pixels = 0.85;
varying float coverage;

void vertex() {
    vec3 p = (MODELVIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;
    vec3 tangent_view = normalize((MODELVIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
    vec3 side = cross(tangent_view, normalize(-p));
    float side_length = length(side);
    side = side_length > 0.0001 ? side / side_length : vec3(1.0, 0.0, 0.0);
    float metres_per_pixel = 2.0 * max(0.01, -p.z) / (PROJECTION_MATRIX[1][1] * VIEWPORT_SIZE.y);
    float true_pixels = UV2.x / metres_per_pixel;
    float width_pixels = max(minimum_pixels, true_pixels);
    coverage = min(1.0, true_pixels / width_pixels);
    VERTEX = p + side * (UV.x - 0.5) * width_pixels * metres_per_pixel;
}

void fragment() {
    // Coverage compensation avoids turning distant wires into black ropes.
    float edge_distance = abs(UV.x * 2.0 - 1.0);
    float aa = max(fwidth(edge_distance), 0.001);
    float edge = 1.0 - smoothstep(1.0 - aa, 1.0, edge_distance);
    ALBEDO = wire_color.rgb;
    ALPHA = edge * coverage * wire_color.a;
}
