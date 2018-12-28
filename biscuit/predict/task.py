from logging import getLogger

import luigi

from . import core, cleaning

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
        for article in core.get_targets(self.date):
            ret.append(PredictArticleTag(self.date, article))

        return ret

    def run(self) -> None:
        pass

    def output(self):
        pass


class PredictArticleTag(luigi.Task):
    date = luigi.DateParameter()
    article = luigi.Parameter()

    def requires(self) -> luigi.Task:
        return DownloadDocument(self.article)

    def run(self) -> None:
        pass

    def output(self):
        return luigi.LocalTarget(
            f"/var/log/biscuit/documents/{self.article.resolved_id}.txt"
        )


class DownloadDocument(luigi.Task):
    article = luigi.Parameter()

    def run(self) -> None:
        doc = core.download_document(self.article)
        text = cleaning.clean(doc)
        with open(self.output().path, 'w+') as f:
            f.write(text)

    def output(self):
        return luigi.LocalTarget(
            f"/var/log/biscuit/documents/{self.article.resolved_id}.txt"
        )
