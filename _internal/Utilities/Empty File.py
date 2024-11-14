"""
We use sine to get a value that oscillates with time. This makes our
camera move back and forth. We can scale time with _Speed to shrink or
grow the period of the oscillation which makes the shake faster or
slower.
Since shakes are tied to time, the _Seed value allows you to offset
shakes so different objects aren't shaking the same. You could set it to
a random value in Start.
var sin = Mathf.Sin(_Speed * (_Seed + Time.time));
We shake along a direction, but use Perlin noise to get an offset. Scale
the noise (which is in [-0.5,0.5]) to adjust the amount of deviation
from our direction.
var direction = _Direction + Get2DNoise(_Seed) * _NoiseMagnitude;
Normalize the result (limit vector length to 1) to ensure we're never
more than _MaxMagnitude away from neutral.
direction.Normalize();
Multiply our bits together to find our position this frame. Since we're
using two continuous functions (sine and perlin), we won't be far off
from where we were last frame.
Additionally, we have a fade value so we can reduce the shake strength
over time.
_Target.localPosition = direction * sin * _MaxMagnitude * _FadeOut;
"""