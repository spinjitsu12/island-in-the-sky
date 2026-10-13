// Copyright (c) 2026 spinjitsu12. All rights reserved.
// Express written permission required; see LICENSE.
shader_type sky;
// Calibration atmosphere. Final volumetric cloud/weather system is a later milestone.
uniform vec3 zenith_color : source_color = vec3(0.20, 0.37, 0.62);
uniform vec3 horizon_color : source_color = vec3(0.82, 0.78, 0.76);
uniform vec3 cloud_color : source_color = vec3(0.92, 0.88, 0.83);

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
	vec2 i = floor(p); vec2 f = fract(p); vec2 u = f*f*(3.0-2.0*f);
	return mix(mix(hash(i), hash(i+vec2(1,0)), u.x), mix(hash(i+vec2(0,1)), hash(i+vec2(1,1)), u.x), u.y);
}
float fbm(vec2 p) {
	float v=0.0; float a=0.5;
	for (int i=0; i<5; i++) { v+=a*noise(p); p=p*2.03+vec2(17.3,8.1); a*=0.5; }
	return v;
}
void sky() {
	float elevation = max(EYEDIR.y, 0.0);
	vec3 color = mix(horizon_color, zenith_color, pow(elevation, 0.55));
	vec2 plane = EYEDIR.xz / max(abs(EYEDIR.y), 0.12);
	float clouds = smoothstep(0.38, 0.72, fbm(plane*1.4));
	float bank = 1.0 - smoothstep(-0.22, 0.08, EYEDIR.y);
	color = mix(color, cloud_color * (0.84 + 0.16*clouds), bank*0.92);
	float upper = smoothstep(0.58, 0.79, fbm(plane*0.7+32.0));
	color = mix(color, cloud_color, upper*0.25*elevation);
	COLOR = color;
}
