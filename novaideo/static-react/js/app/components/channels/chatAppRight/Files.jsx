/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { Translate } from 'react-redux-i18n';
import InsertDriveFileIcon from 'material-ui-icons/InsertDriveFile';
import { graphql } from 'react-apollo';

import { commentsQuery } from '../../../graphql/queries';
import { COMMENTS_ACTIONS, ACTIONS } from '../../../processes';

import DetailsSection from './DetailsSection';
import { RenderComments } from '../Comments';

const styles = (theme) => {
  return {
    container: {
      height: '100% !important'
    },
    list: {
      height: '100%'
    },
    counter: {
      fontFamily: 'LatoWebLight',
      fontWeight: 100,
      marginLeft: 5,
      fontSize: 14
    },
    sectionIcon: {
      color: theme.palette.warning[500]
    },
    sectionIconActive: {
      '&:hover': {
        color: theme.palette.warning[500]
      }
    }
  };
};

class Files extends React.Component {
  render() {
    const { data, id, channel, classes, onOpen, open } = this.props;
    const totalCount = data.node && data.node.comments && data.node.comments.totalCount;
    return (
      <DetailsSection
        id={id}
        classes={{
          sectionIcon: classes.sectionIcon,
          sectionIconActive: classes.sectionIconActive
        }}
        onOpen={onOpen}
        open={open}
        title={
          <span>
            {<Translate value="channels.filesBlockTitle" count={totalCount} />}
          </span>
        }
        Icon={InsertDriveFileIcon}
      >
        {open &&
          <RenderComments
            rightDisabled
            customScrollbar
            dynamicDivider={false}
            displayForm={false}
            data={data}
            channelId={channel.id}
            filter={{ file: true }}
            classes={{ container: classes.container, list: classes.container }}
          />}
      </DetailsSection>
    );
  }
}

export default withStyles(styles, { withTheme: true })(
  graphql(commentsQuery, {
    options: (props) => {
      return {
        fetchPolicy: 'cache-and-network',
        notifyOnNetworkStatusChange: true,
        variables: {
          filter: '',
          pinned: false,
          file: true,
          first: 25,
          after: '',
          id: props.channel.id,
          processIds: [],
          nodeIds: [],
          processTags: [],
          actionTags: [ACTIONS.primary],
          subjectActionsNodeIds: COMMENTS_ACTIONS
        }
      };
    }
  })(Files)
);