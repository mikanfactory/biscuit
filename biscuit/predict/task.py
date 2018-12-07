from logging import getLogger

import luigi

from . import core

logger = getLogger('biscuit.task')


class Invoke(luigi.WrapperTask):
    date = luigi.DateParameter()

    def requires(self) -> luigi.Task:
        return AddTagsToAllItems(self.date)


class AddTagsToAllItems(luigi.Task):
    date = luigi.DateParameter()

    def requires(self) -> luigi.Task:
        return GatherTagsForAllItems(self.date)


class GatherTagsForAllItems(luigi.Task):
    date = luigi.DateParameter()

    def requires(self) -> luigi.Task:
        ret = []
        for item in core.get_targets(self.date):
            ret.append(PredictTagForItem(self.date, item))

        return ret


class PredictTagForItem(luigi.Task):
    date = luigi.DateParameter()
    item = luigi.Parameter()

    def requires(self) -> luigi.Task:
        return DownloadMetadata(self.date, self.item)


class DownloadMetadata(luigi.Task):
    date = luigi.DateParameter()
    item = luigi.Parameter()

    def run(self) -> None:
        pass

    def output(self):
        pass
