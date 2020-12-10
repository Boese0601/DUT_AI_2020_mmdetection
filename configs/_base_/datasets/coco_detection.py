dataset_type = 'CocoDataset'  ##underwater
data_root = 'data/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
## ??
albu_train_transforms = [
    dict(type='RandomRotate90', always_apply=False, p=0.5),
    dict(type='Cutout',num_holes=8, max_h_size=8, max_w_size=8, fill_value=0, always_apply=False, p=0.5),
]
##
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
   ##??
    dict(type='Albu',
         transforms=albu_train_transforms,
         bbox_params=dict(
         type='BboxParams',
         format='pascal_voc',
         label_fields=['gt_labels'],
         min_visibility=0.0,
         filter_lost_elements=True),
     keymap={
         'img': 'image',
         'gt_masks': 'masks',
         'gt_bboxes': 'bboxes'
     },
     update_pad_shape=False,
     skip_img_without_anno=True),
    dict(type='BBoxJitter_ratio', x_ratio=0.03, y_ratio=0.03, prob=0.5),
     ##？？
    dict(type='Resize', img_scale=[(4096,800),(4096,1200)],multiscale_mode='range', keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=[(4096, 800), (4096, 1000), (4096, 1200)],##(1333,800)
        flip=True,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=1,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        ann_file=data_root + 'train/annotations/train.json',
        img_prefix=data_root + 'train/image/',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'val/annotations/val.json',
        img_prefix=data_root + 'val/image/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        ann_file=data_root + 'test/annotations/test.json',
        img_prefix=data_root + 'test/image/',
        pipeline=test_pipeline))
evaluation = dict(interval=1, metric='bbox')
