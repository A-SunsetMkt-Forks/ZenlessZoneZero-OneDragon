import time

from one_dragon.base.operation.operation_edge import node_from
from one_dragon.base.operation.operation_node import operation_node
from one_dragon.base.operation.operation_round_result import OperationRoundResult
from one_dragon.utils.i18_utils import gt
from zzz_od.context.zzz_context import ZContext
from zzz_od.hollow_zero.event import resonium_utils
from zzz_od.operation.zzz_operation import ZOperation


class ChooseResonium(ZOperation):

    def __init__(self, ctx: ZContext):
        """
        在选择鸣徽的画面了 选择一个
        :param ctx:
        """
        ZOperation.__init__(
            self, ctx,
            op_name=gt('选择鸣徽', 'game')
        )

    @operation_node(name='选择', is_start_node=True)
    def choose_one(self) -> OperationRoundResult:
        item_list = resonium_utils.get_to_choose_list(self.ctx, self.last_screenshot, '选择')
        if len(item_list) == 0:
            return self.round_retry(status='识别不到选项', wait=0.5)

        idx_list = resonium_utils.choose_resonium_by_priority([i.data for i in item_list],
                                                              self.ctx.hollow_zero_challenge_config.resonium_priority)
        if len(idx_list) == 0:
            if len(item_list) >= 3:  # 如果都识别到了 那证明就是没有匹配到优先级
                return self.round_fail(status='优先级无返回')
            else:
                return self.round_retry(status='优先级无返回', wait=0.5)

        mr = item_list[idx_list[0]]
        self.ctx.controller.click(mr.center)
        time.sleep(0.1)
        return self.round_by_click_area('零号空洞-事件', '空白', success_wait=0.9)

    @node_from(from_name='选择', success=False)  # 防止识别有问题 兜底随便选一个
    @operation_node(name='兜底选择')
    def choose_default(self):
        area = self.ctx.screen_loader.get_area('零号空洞-事件', '底部-选择列表')
        return self.round_by_ocr_and_click(self.last_screenshot, '选择', area=area,
                                           success_wait=1, retry_wait=1,
                                           color_range=[(240, 240, 240), (255, 255, 255)])






def __debug():
    ctx = ZContext()
    ctx.init_by_config()
    ctx.start_running()
    ctx.init_ocr()
    op = ChooseResonium(ctx)
    op.execute()


if __name__ == '__main__':
    __debug()