checkpoint_config = dict(interval=1)
# yapf:disable
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from =  'pretrain/cascade_rcnn_x101_32x4d_fpn_1x_coco_20200316.pth'
resume_from = 'work_dirs/cascade_rcnn_x101_32x4d_fpn_1x_coco/epoch_9.pth'
workflow = [('train', 1)]
