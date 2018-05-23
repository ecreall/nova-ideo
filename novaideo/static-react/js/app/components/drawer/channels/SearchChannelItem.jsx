/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Icon from '@material-ui/core/Icon';
import CreateIcon from '@material-ui/icons/Create';
import { connect } from 'react-redux';
import classNames from 'classnames';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';
import { convertFromRaw } from 'draft-js';

import { addPrivateChannel } from '../../../graphql/processes/commentProcess';
import AddPrivateChannel from '../../../graphql/processes/commentProcess/mutations/AddPrivateChannel.graphql';
import { goTo, get } from '../../../utils/routeMap';
import UserAvatar from '../../user/UserAvatar';
import { openCollaborationRight } from '../../../actions/collaborationAppActions';
import { CONTENTS_IDS } from '../../collaborationApp/collaborationAppRight';
import { ListItem, ListItemIcon, ListItemText } from '../../styledComponents/List';

const styles = (theme) => {
  return {
    listItem: {
      paddingTop: '5px !important',
      marginLeft: '0 !important',
      paddingBottom: '5px !important'
    },
    text: {
      fontSize: 17,
      padding: 0,
      whiteSpace: 'nowrap',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      fontWeight: 600
    },
    icon: {
      width: 27,
      height: 27,
      marginRight: 7,
      fontSize: '17px !important'
    },
    avatar: {
      width: 27,
      height: 27,
      marginRight: 7,
      borderRadius: 4
    },
    avatarNoPicture: {
      fontSize: 17,
      backgroundColor: theme.palette.primary['500'],
      color: 'white'
    }
  };
};

export class DumbSearchChannelItem extends React.Component {
  state = {
    loading: false
  };

  open = () => {
    const { node, addChannel } = this.props;
    if (node.channel) {
      this.gotoChannel(node.channel);
    } else {
      this.setState({ loading: true }, () => {
        addChannel({
          context: node.subject
        }).then((result) => {
          if (result) {
            this.setState({ loading: false }, () => {
              this.gotoChannel(result.data.addPrivateChannel.channel);
            });
          }
        });
      });
    }
  };

  gotoChannel = (channel) => {
    const { chatAppIntegreted, itemProps: { onClick } } = this.props;
    if (chatAppIntegreted) {
      this.props.openCollaborationRight({
        componentId: CONTENTS_IDS.chat,
        props: { channel: channel.id, channelTitle: channel.title }
      });
    } else {
      goTo(get('messages', { channelId: channel.id }));
    }
    if (onClick) onClick();
  };

  renderIcon = () => {
    const { node, currentMessage, classes } = this.props;
    const { loading } = this.state;
    if (loading) {
      return (
        <ListItemIcon>
          <CircularProgress size={27} style={{ color: 'white' }} />
        </ListItemIcon>
      );
    }
    const channelPicture = node.subject.picture;
    const editor = currentMessage && currentMessage.values && currentMessage.values.comment;
    const hasMessage = editor && convertFromRaw(editor).getPlainText();
    if (hasMessage) {
      return (
        <ListItemIcon>
          <CreateIcon className={classNames('menu-item-icon', classes.icon)} />
        </ListItemIcon>
      );
    }
    return 'picture' in node.subject
      ? <UserAvatar
        picture={channelPicture}
        classes={{ avatar: classes.avatar, noPicture: classes.avatarNoPicture }}
        title={node.subject.title}
      />
      : <ListItemIcon>
        <Icon className={classNames('menu-item-icon mdi-set mdi-pound', classes.icon)} />
      </ListItemIcon>;
  };

  render() {
    const { node, classes, theme } = this.props;
    return (
      <ListItem
        hoverColor={theme.palette.info[500]}
        onClick={this.open}
        dense
        button
        ContainerComponent="div"
        classes={{
          root: classes.listItem
        }}
      >
        {this.renderIcon()}
        <ListItemText
          classes={{ primary: classNames('menu-item-text', classes.text) }}
          className={classes.text}
          primary={node.subject.title}
        />
      </ListItem>
    );
  }
}

export const mapDispatchToProps = {
  openCollaborationRight: openCollaborationRight
};

export const mapStateToProps = (state, props) => {
  return {
    currentMessage: state.form[props.node.channel && props.node.channel.id],
    chatAppIntegreted: state.apps.chatApp.integrations
  };
};

export default withStyles(styles, { withTheme: true })(
  graphql(AddPrivateChannel, {
    props: function (props) {
      return {
        addChannel: addPrivateChannel(props)
      };
    }
  })(connect(mapStateToProps, mapDispatchToProps)(DumbSearchChannelItem))
);