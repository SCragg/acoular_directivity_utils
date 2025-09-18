import acoular as ac
import numpy as np

ac.config.global_caching = 'none'

# A test script showing ambisonic reciever working with multiple signals in a scene

def main():

    f_sample = 44100
    num_samples = f_sample * 5

    sine_signal_1 = ac.SineGenerator(freq=400, sample_freq=f_sample, num_samples=num_samples)
    sine_signal_2 = ac.SineGenerator(freq=547, sample_freq=f_sample, num_samples=num_samples)

    # Simple environment
    e = ac.Environment(c=343.0)

    # Define the microphone
    m = ac.MicGeomDirectional()
    m.pos_total = np.array([[0],[0],[0]]) # Mic placed in centre of the scene

    # Spherical Harmonic Directivity is used with a single microphone to generate the audio channels
    sh_dir = ac.SphericalHarmonicDirectivity()
    sh_dir.n = 3
    sh_dir.orientation = np.eye(3)

    m.directivities_total = [sh_dir]

    sine_gen_1 = ac.PointSourceDirectional(
        signal=sine_signal_1,  # the signal of the source
        mics=m,  # set the "array" with which to measure the sound field
        loc=(-20, 0, 0),  # location of the source
        directivity=ac.OmniDirectivity(orientation=np.eye(3)),
        env=e,
    )

    sine_gen_2 = ac.PointSourceDirectional(
        signal=sine_signal_2,  # the signal of the source
        mics=m,  # set the "array" with which to measure the sound field
        loc=(20, 0, 0),  # location of the source
        directivity=ac.OmniDirectivity(orientation=np.eye(3)),
        env=e,
    )

    mixture = ac.Mixer(source=sine_gen_1, sources=[sine_gen_2])

    # Using a Spherical Harmonic Reciever will generate extra output channels
    # This is based on the order of the reciever
    channels = list(range(ac.num_channels_for_sph_degree(sh_dir.n)))


    # Prepare wav output.
    output1 = ac.WriteWAV(file='output_1.wav',
                         source=sine_gen_1, 
                         channels=channels)
    
    output2 = ac.WriteWAV(file='output_2.wav',
                        source=sine_gen_2, 
                        channels=channels)

    output3 = ac.WriteWAV(file='mixture.wav',
                    source=mixture, 
                    channels=channels)

    from time import perf_counter

    tic = perf_counter()
    output1.save()
    output2.save()
    output3.save()
    print('Computation time: ', perf_counter() - tic)


if __name__ == '__main__':
    main()