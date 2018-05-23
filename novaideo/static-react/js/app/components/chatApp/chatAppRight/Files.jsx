import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { Translate, I18n } from 'react-redux-i18n';
import { graphql } from 'react-apollo';

import { iconAdapter } from '../../../utils/globalFunctions';
import Comments from '../../../graphql/queries/Comments.graphql';
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
    },
    noResult: {
      paddingLeft: 25,
      marginBottom: 15,
      fontSize: 15,
      color: '#717274',
      lineHeight: '20px'
    }
  };
};

const Files = ({ data, id, channel, classes, onOpen, open }) => {
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
      Icon={iconAdapter('mdi-set mdi-file-outline')}
    >
      {open &&
        <RenderComments
          rightDisabled
          dynamicDivider={false}
          displayForm={false}
          displayFooter={false}
          data={data}
          moreBtn={
            <span>
              {I18n.t('common.moreResult')}
            </span>
          }
          NoItems={() => {
            return (
              <div className={classes.noResult}>
                {I18n.t('channels.noFilesBlock')}
              </div>
            );
          }}
          channelId={channel.id}
          filter={{ file: true }}
          classes={{ container: classes.container, list: classes.container }}
        />}
    </DetailsSection>
  );
};

export default withStyles(styles, { withTheme: true })(
  graphql(Comments, {
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