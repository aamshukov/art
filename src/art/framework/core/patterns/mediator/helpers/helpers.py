#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator domain helper """
from art.framework.core.diagnostics.code import Code
from art.framework.core.diagnostics.status import Status
from art.framework.core.domain.base import Base
from art.framework.core.result.result import Result


class MediatorDomainHelper(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def send(context, bindings):
        """
        """
        # propagate down
        for binding in bindings:
            result = binding.middleware.handle(context)
            if result.status.custom_code == Code.Aborted:
                break
        else:
            # propagate up (bubble up)
            for binding in reversed(bindings):
                result = binding.middleware.handle(context)
                if result.status.custom_code == Code.Aborted:
                    break
        if all(result.status.custom_code == Code.Success for result in context.results):
            return Result(Status(), context)
        else:
            return Result(Status(custom_code=Code.Attention), data=context)

    @staticmethod
    async def send_async(context, bindings):
        """
        """
        # propagate down
        for binding in bindings:
            result = await binding.middleware.handle_async(context)
            if result.status.custom_code == Code.Aborted:
                break
        else:
            # propagate up (bubble up)
            for binding in reversed(bindings):
                result = await binding.middleware.handle_async(context)
                if result.status.custom_code == Code.Aborted:
                    break
        if all(result.status.custom_code == Code.Success for result in context.results):
            return Result(Status(), context)
        else:
            return Result(Status(custom_code=Code.Attention), data=context)
