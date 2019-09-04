def get_config():
    base_directory = './data/maps_piano/data'
    metadata_filename = './maps-metadata-non-overlapping.csv'
    for batchsize in [256]:
        for lr in [0.15]:
            config = dict(
                run_id='ofos/lr_{}_bs_{}'.format(lr, batchsize),
                modules=dict(
                    run=dict(
                        name='runners.default_runner',
                        args=dict()
                    ),
                    net=dict(
                        name='models.ofos'
                    ),
                    dataloader=dict(
                        name='dataloaders.ofos',
                        offset_suppression=False,
                        input_context=dict(
                            frame_size=11,
                            hop_size=1,
                            origin='center'
                        ),
                        target_maxfilter=dict(
                            y_onsets=3,
                            y_frames=1,
                            y_offsets=3
                        ),
                        args=dict(
                            train=dict(
                                base_directory=base_directory,
                                metadata_filename=metadata_filename,
                                split='train',
                                sampler='RandomSampler'
                            ),
                            valid=dict(
                                individual_files=True,
                                base_directory=base_directory,
                                metadata_filename=metadata_filename,
                                split='validation',
                                sampler='SequentialSampler'
                            ),
                            test=dict(
                                individual_files=True,
                                base_directory=base_directory,
                                metadata_filename=metadata_filename,
                                split='test',
                                sampler='SequentialSampler'
                            ),
                        )
                    )
                ),
                debug=dict(
                    weights=False,
                    gradients=False
                ),
                batchsize=batchsize,
                n_epochs=100,
                optimizer=dict(
                    name='SGD',
                    params=dict(
                        lr=lr,
                        momentum=0.9,
                        nesterov=True
                    )
                ),
                lambdas=dict(
                    y_onsets=1,
                    y_frames=1,
                    y_offsets=1
                ),
                scheduler=dict(
                    name='ReduceLROnPlateau',
                    params=dict(
                        mode='max',
                        factor=0.1,
                        patience=10,
                        verbose=True,
                        threshold=1e-2
                    )
                ),
                audio_options=dict(
                    num_channels=1,
                    sample_rate=44100,
                    spectrogram_type='LogarithmicFilteredSpectrogram',
                    filterbank='LogarithmicFilterbank',
                    frame_size=4096,
                    fft_size=4096,
                    hop_size=441 * 2,  # 50 fps
                    num_bands=24,
                    fmin=30,
                    fmax=10000.0,
                    fref=440.0,
                    norm_filters=True,
                    unique_filters=True,
                    circular_shift=False,
                    add=1
                )
            )
            yield config
