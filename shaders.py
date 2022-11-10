vertex_shader ='''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 norms;
out vec3 pos;

void main()
{
    UVs = texcoords;
    norms = normals;
    pos = (modelMatrix * vec4(position + normals * sin(time * 3)/10, 1.0)).xyz;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position + normals * sin(time * 3)/10, 1.0);

}
'''

fragment_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;

uniform sampler2D tex;

void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));

    fragColor = texture(tex, UVs) * intensity;
}
'''

toon_shader = '''
uniform vec3 lightDir;
varying vec3 normal;
out vec4 fragColor;

void main()
{
	float intensity;
	vec4 color;
	intensity = dot(lightDir,normal);

	if (intensity > 0.95)
		color = vec4(1.0,0.5,0.5,1.0);
	else if (intensity > 0.5)
		color = vec4(0.6,0.3,0.3,1.0);
	else if (intensity > 0.25)
		color = vec4(0.4,0.2,0.2,1.0);
	else
		color = vec4(0.2,0.1,0.1,1.0);
	fragColor = color;

}
'''
bow_shader = '''
#version 330

layout (location = 0) in vec3 Position;

uniform mat4 gScaling;

out vec4 Color;

const vec4 colors[3] = vec4[3]( vec4(1, 0, 0, 1),
                                vec4(0, 1, 0, 1),
                                vec4(0, o, 1, 1) );
void main(){
    gl_Position = gScaling * vec4(Position, 1.0);
    Color = colors[gl_VertexID];
}
'''
gurad_shader = '''
uniform mat4 u_MVPMatrix;    
uniform mat4 u_MVMatrix;      
uniform vec3 u_LightPos;      
 
attribute vec4 a_Position;    
attribute vec4 a_Color;       
attribute vec3 a_Normal;     
 
varying vec4 v_Color;         
 
void main()
{
    
    vec3 modelViewVertex = vec3(u_MVMatrix * a_Position);
 
    vec3 modelViewNormal = vec3(u_MVMatrix * vec4(a_Normal, 0.0));
 
    float distance = length(u_LightPos - modelViewVertex);
 
    vec3 lightVector = normalize(u_LightPos - modelViewVertex);
 
    float diffuse = max(dot(modelViewNormal, lightVector), 0.1);

    diffuse = diffuse * (1.0 / (1.0 + (0.25 * distance * distance)));
 
    v_Color = a_Color * diffuse;
 
    gl_Position = u_MVPMatrix * a_Position;
}
'''