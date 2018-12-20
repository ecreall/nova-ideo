import React from 'react';
import { Query, graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import { I18n } from 'react-redux-i18n';
import Badge from '@material-ui/core/Badge';
import NotificationsIcon from '@material-ui/icons/Notifications';
import Divider from '@material-ui/core/Divider';
import debounce from 'lodash.debounce';

import { markAlertsAsRead as markAsRead } from '../../graphql/processes/common';
import MarkAlertsAsRead from '../../graphql/processes/common/mutations/MarkAlertsAsRead.graphql';
import AlertsQuery from '../../graphql/queries/Alerts.graphql';
import { Menu } from '../common/menu';
import FlatList from '../common/FlatList';
import Alert from './Alert';

const styles = {
  container: {
    padding: 5
  },
  menuPaper: {
    maxHeight: 400
  }
};

class AlertsContent extends React.Component {
  state = {
    open: false
  };

  componentDidUpdate() {
    const {
      data, userId, newAlerts, markAlertsAsRead
    } = this.props;
    const { open } = this.state;
    if (open && data) {
      const { data: { person: { alerts: { edges } } } } = data;
      const alertsIds = edges.map((alert) => {
        return alert.node.id;
      });
      const newSubAlerts = newAlerts.filter((alert) => {
        return alertsIds.includes(alert);
      });
      if (newSubAlerts.length > 0) {
        debounce(() => {
          markAlertsAsRead({ alerts: newSubAlerts, userId: userId });
        }, 2000)();
      }
    }
  }

  open = () => {
    this.setState({ open: true });
  };

  close = () => {
    this.setState({ open: false });
  };

  render() {
    const {
      data, newAlerts, totalCount, classes
    } = this.props;
    return (
      <Menu
        id="alert-menu"
        classes={{ menuPaper: classes.menuPaper }}
        onOpen={this.open}
        onClose={this.close}
        activator={(
          <IconButton>
            {totalCount > 0 ? (
              <Badge badgeContent={totalCount} color="error">
                <NotificationsIcon />
              </Badge>
            ) : (
              <NotificationsIcon />
            )}
          </IconButton>
        )}
      >
        <FlatList
          data={data}
          getEntities={(entities) => {
            return entities.data ? entities.data.person.alerts : entities.person.alerts;
          }}
          ListItem={Alert}
          moreBtn={<span>{I18n.t('common.moreResult')}</span>}
          Divider={Divider}
          itemProps={{
            newAlerts: newAlerts
          }}
        />
      </Menu>
    );
  }
}

export const AlertsContentWithStyle = withStyles(styles)(
  graphql(MarkAlertsAsRead, {
    props: function (props) {
      return {
        markAlertsAsRead: markAsRead(props)
      };
    }
  })(AlertsContent)
);

const Alerts = ({ userId }) => {
  return (
    <Query
      notifyOnNetworkStatusChange
      query={AlertsQuery}
      variables={{
        id: userId,
        first: 15,
        after: ''
      }}
    >
      {(result) => {
        const newAlerts = (result.data && result.data.person && result.data.person.unreadAlertsIds) || [];
        const totalCount = newAlerts.length;
        return <AlertsContentWithStyle userId={userId} data={result} newAlerts={newAlerts} totalCount={totalCount} />;
      }}
    </Query>
  );
};

export default Alerts;