from logging import getLogger

import luigi

from . import core

logger = getLogger('biscuit.task')


class Invoke(luigi.WrapperTask):
    date = luigi.DateParameter()

    def requires(self) -> luigi.Task:
        return AddTagToAllArticles(self.date)


class AddTagToAllArticles(luigi.Task):
    date = luigi.DateParameter()

    def requires(self) -> luigi.Task:
        return GatherArticleTags(self.date)

    def run(self) -> None:
        pass

    def output(self):
        pass


class GatherArticleTags(luigi.Task):
    date = luigi.DateParameter()

    def requires(self) -> luigi.Task:
        ret = []
        for item in core.get_targets(self.date):
            ret.append(PredictArticleTag(self.date, item))

        return ret

    def run(self) -> None:
        pass

    def output(self):
        pass


class PredictArticleTag(luigi.Task):
    date = luigi.DateParameter()
    item = luigi.Parameter()

    def requires(self) -> luigi.Task:
        return DownloadDocument(self.date, self.item)

    def run(self) -> None:
        pass

    def output(self):
        pass


class DownloadDocument(luigi.Task):
    date = luigi.DateParameter()
    item = luigi.Parameter()

    def run(self) -> None:
        pass

    def output(self):
        pass
