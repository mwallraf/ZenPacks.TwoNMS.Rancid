(function(){

var ZC = Ext.ns('Zenoss.component');

function makeUrl(obj)  {
    return "TEST";
}

// TODO: inverse sort on revision id
// TODO: on-click make sure the Rancid link is selected by default
ZC.RancidRevisionPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'RancidRevision',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'monitored'},
                {name: 'rRevisionId'}, 
                {name: 'rRevisionDate'},
                {name: 'rRancidViewerLink'},
            ],
            columns: [
           {
                id: 'rRevisionId',
                dataIndex: 'rRevisionId',
                header: _t('Revision ID'),
                sortable: true,
            },{
                id: 'rRevisionDate',
                dataIndex: 'rRevisionDate',
                header: _t('Date'),
                sortable: true,
                width: 300
            },{
                id: 'rRancidViewerLink',
                dataIndex: 'rRancidViewerLink',
                header: _t('External link'),
                width: 300,
                renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                    var returnString = "<a href=" + record.get("rRancidViewerLink") + " target='_blank'> Viewer </a>";
                    return returnString;
                },
            }
            ]

        });
        ZC.RancidRevisionPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('RancidRevisionPanel', ZC.RancidRevisionPanel);
ZC.registerName('RancidRevision', _t('Rancid Config'), _t('Rancid Configs'));


    
})();


