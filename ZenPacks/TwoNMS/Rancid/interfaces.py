from Products.Zuul.form import schema
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.interfaces.template import IRRDDataSourceInfo
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.ZenModel.ZVersion import VERSION as ZENOSS_VERSION
from Products.ZenUtils.Version import Version

if Version.parse('Zenoss %s' % ZENOSS_VERSION) >= Version.parse('Zenoss 4'):
    SingleLineText = schema.TextLine
    MultiLineText = schema.Text
else:
    SingleLineText = schema.Text
    MultiLineText = schema.TextLine


class IRancidRevisionInfo(IComponentInfo):
    rRevisionId = SingleLineText(title=_t(u"Revision ID"), readonly=True, group="Details")
    rRevisionDate = SingleLineText(title=_t(u"Revision Date"), readonly=True, group="Details")
    rRancidViewerLink = SingleLineText(title=_t(u"External Viewer"), readonly=False, group="Details")
    #rRevisionFilePath = ""
    #rRevisionCatPath = ""
