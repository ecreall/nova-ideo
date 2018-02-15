/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';
import { CircularProgress } from 'material-ui/Progress';

import AllignedActions from '../common/AllignedActions';
import { getActions, filterActions } from '../../utils/entities';
import { goTo, get } from '../../utils/routeMap';
import { getFormattedDate } from '../../utils/globalFunctions';
import UserActionsWrapper from './UserActionsWrapper';
import { closeChatApp } from '../../actions/actions';
import { personInfoQuery } from '../../graphql/queries';
import Comment from '../forms/Comment';
import { PROCESSES, ACTIONS } from '../../constants';

const imgGradient =
  'linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0) 34%, rgba(0,0,0,0.2) 66%, rgba(0,0,0,0.2) 83%, rgba(0,0,0,0.6)),';

const styles = {
  container: {
    position: 'relative',
    minWidth: 320,
    maxWidth: 450,
    marginBottom: 5,
    '&:hover': {
      backgroundColor: '#f9f9f9'
    }
  },
  header: {
    margin: '10px 0',
    position: 'absolute',
    opacity: 1,
    pointerEvents: 'none',
    left: 20,
    bottom: 5,
    color: 'white'
  },
  headerTitle: {
    fontSize: 20,
    color: 'white',
    fontWeight: '900',
    marginBottom: 5
  },
  headerAddOn: {
    color: 'white',
    fontSize: 13
  },
  body: {
    display: 'flex',
    flexDirection: 'column',
    padding: '15px 20px',
    maxWidth: '100%'
  },
  bodyContent: {
    display: 'flex',
    justifyContent: 'space-between',
    flexDirection: 'column',
    width: '100%',
    height: '100%'
  },
  bodyFooter: {
    display: 'flex',
    flexDirection: 'row',
    marginTop: 15
  },
  text: {
    '& a': {
      color: '#0576b9',
      textDecoration: 'none',
      '&:hover': {
        textDecoration: 'underline'
      }
    },
    '& p': {
      margin: 0
    }
  },
  progress: {
    width: '100%',
    minWidth: 320,
    minHeight: 340,
    display: 'flex',
    justifyContent: 'center'
  },
  formContainer: {
    padding: 10,
    paddingRight: 10,
    paddingLeft: 10,
    backgroundColor: '#ededed',
    boxShadow: '0 -1px 0 rgba(0,0,0,.1)'
  },
  imgContainer: {
    borderTopRightRadius: 6,
    borderBottomRightRadius: 0,
    borderBottomLeftRadius: 0,
    borderTopLeftRadius: 6,
    backgroundClip: ' padding-box',
    margin: 0,
    height: 224,
    position: 'relative'
  },
  img: {
    cursor: 'pointer',
    borderTopRightRadius: 6,
    borderBottomRightRadius: 0,
    borderBottomLeftRadius: 0,
    borderTopLeftRadius: 6,
    backgroundClip: ' padding-box',
    margin: 0,
    height: 224,
    backgroundPosition: '0 -448px,0 -48px,0 -48px',
    backgroundSize: '100% 300%,100%,100%,100%',
    transition: 'background-position 150ms ease'
  }
};

export class RenderUserPopover extends React.Component {
  constructor(props) {
    super(props);
    this.menu = null;
  }

  onMouseOver = () => {
    if (this.menu) this.menu.open();
  };

  onMouseLeave = () => {
    if (this.menu) this.menu.close();
  };

  openDetails = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
    this.props.closeChatApp();
    goTo(get('users', { userId: this.props.data.person.id }));
  };

  onCommentSubmit = () => {
    const { onActionClick, data: { person } } = this.props;
    if (onActionClick) onActionClick();
    setTimeout(() => {
      goTo(get('messages', { channelId: person.channel.id }, { right: 'info' }));
    }, 200);
  };

  render() {
    const { data, classes } = this.props;
    if (data.loading) {
      return (
        <div className={classes.progress}>
          <CircularProgress size={30} />
        </div>
      );
    }
    const person = data.person;
    const authorPicture = person && person.picture;
    const isAnonymous = person && person.isAnonymous;
    const createdAtF = getFormattedDate(person.createdAt, 'date.format');
    const communicationActions = getActions(person.actions, { descriminator: ACTIONS.communication });
    const commentAction = filterActions(communicationActions, { behaviorId: PROCESSES.usermanagement.nodes.discuss.nodeId })[0];
    const channel = person.channel;
    const channelId = channel ? channel.id : `${person.id}-channel`;
    return [
      <div className={classes.container} onMouseOver={this.onMouseOver} onMouseLeave={this.onMouseLeave}>
        <div className={classes.imgContainer}>
          <div
            className={classes.img}
            style={{
              backgroundImage: `${imgGradient} url('${authorPicture && authorPicture.url}')`
            }}
          />
          <div className={classes.header}>
            <div className={classes.headerTitle}>
              {person.title}
            </div>
            {!isAnonymous &&
              <div className={classes.headerAddOn}>
                {createdAtF}
              </div>}
          </div>
        </div>
        <div className={classes.body}>
          <div className={classes.bodyContent}>
            <div className={classes.text} dangerouslySetInnerHTML={{ __html: person.description }} />
            <div className={classes.bodyFooter}>
              <AllignedActions actions={communicationActions} onActionClick={this.props.actionsManager.performAction} />
            </div>
          </div>
        </div>
      </div>,
      commentAction
        ? <Comment
          isDiscuss
          classes={{ container: classes.formContainer }}
          key={channelId}
          form={channelId}
          action={commentAction}
          context={person.oid}
          subject={person.oid}
          channel={person.channel}
          onSubmit={this.onCommentSubmit}
        />
        : null
    ];
  }
}

export const mapDispatchToProps = {
  closeChatApp: closeChatApp
};

function DumbUserPopover(props) {
  const { data, onActionClick } = props;
  return (
    <UserActionsWrapper person={data.person} onActionClick={onActionClick}>
      <RenderUserPopover {...props} />
    </UserActionsWrapper>
  );
}

export default withStyles(styles)(
  connect(null, mapDispatchToProps)(
    graphql(personInfoQuery, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-and-network',
          variables: { id: props.id }
        };
      }
    })(DumbUserPopover)
  )
);