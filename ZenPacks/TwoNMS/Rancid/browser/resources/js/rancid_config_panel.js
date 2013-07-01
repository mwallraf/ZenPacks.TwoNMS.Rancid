Zenoss.nav.appendTo('Component', [{
        nodeType: 'subselect',
    id: 'rancid_revision_bottom_panel_',
    text: _t('Rancid Details'),
    permission: false,
    userCanModify: false,

        action: function(node, target, combo) {
            var uid = combo.contextUid,
                cardid = 'rancid_revision_config_panel',
                revs = {
                    id: cardid,
                    //xtype: 'basedetailform',
                    xtype: 'backcompat',
                    viewName: 'rancid_view_config_template',
                    text: _t('rancid_revision_config_panel'),
                };

            if (!Ext.get('rancid_revision_config_panel')) {
              target.add(revs);
           }

           target.layout.setActiveItem(cardid);
           target.layout.activeItem.setContext(uid);
       }
}]);
    
    
