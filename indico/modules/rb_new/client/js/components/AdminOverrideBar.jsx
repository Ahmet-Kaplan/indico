/* This file is part of Indico.
 * Copyright (C) 2002 - 2019 European Organization for Nuclear Research (CERN).
 *
 * Indico is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 3 of the
 * License, or (at your option) any later version.
 *
 * Indico is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Indico; if not, see <http://www.gnu.org/licenses/>.
 */

import React from 'react';
import PropTypes from 'prop-types';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import {Icon, Popup} from 'semantic-ui-react';
import {Translate} from 'indico/react/i18n';
import {actions as userActions, selectors as userSelectors} from '../common/user';

import './AdminOverrideBar.module.scss';


const AdminOverrideBar = ({visible, disable}) => {
    if (!visible) {
        return null;
    }

    const trigger = (
        <span>
            <Icon name="exclamation triangle" />
            <Translate>
                Admin override enabled
            </Translate>
        </span>
    );

    return (
        <header styleName="admin-override-bar">
            <Popup trigger={trigger}>
                <Translate>
                    While in Admin Override mode, you can book any room regardless
                    of restrictions and edit any booking.
                </Translate>
            </Popup>
            <span styleName="disable" onClick={disable}>
                <Popup trigger={<Icon name="close" />}>
                    <Translate>
                        Disable admin override
                    </Translate>
                </Popup>
            </span>
        </header>
    );
};

AdminOverrideBar.propTypes = {
    visible: PropTypes.bool.isRequired,
    disable: PropTypes.func.isRequired,
};

export default connect(
    state => ({
        visible: userSelectors.isUserAdminOverrideEnabled(state),
    }),
    dispatch => ({
        disable: bindActionCreators(userActions.toggleAdminOverride, dispatch),
    })
)(AdminOverrideBar);
