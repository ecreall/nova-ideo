import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { Translate, I18n } from 'react-redux-i18n';
import { graphql } from 'react-apollo';

import Comments from '../../../graphql/queries/Comments.graphql';
import { COMMENTS_ACTIONS, ACTIONS } from '../../../processes';
import DetailsSection from './DetailsSection';
import { iconAdapter } from '../../../utils/globalFunctions';
import { RenderComments } from '../Comments';

const styles = (theme) => {
  return {
    container: {
      height: '100% !important'
    },
    list: {
      height: '100%'
    },
    sectionIcon: {
      marginTop: -3,
      fontSize: '22px !important',
      color: theme.palette.danger[500]
    },
    sectionIconActive: {
      '&:hover': {
        color: theme.palette.danger[500]
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

export const DumbPinned = ({ id, channel, classes, onOpen, open, data }) => {
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
      title={<span>{<Translate value="channels.pinnedBlockTitle" count={totalCount} />}</span>}
      Icon={iconAdapter('mdi-set mdi-pin')}
    >
      {open && (
        <RenderComments
          rightDisabled
          dynamicDivider={false}
          displayForm={false}
          displayFooter={false}
          NoItems={() => {
            return <div className={classes.noResult}>{I18n.t('channels.noPinnedBlock')}</div>;
          }}
          data={data}
          channelId={channel.id}
          moreBtn={<span>{I18n.t('common.moreResult')}</span>}
          filter={{ pinned: true }}
          classes={{ container: classes.container, list: classes.container }}
        />
      )}
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
          pinned: true,
          file: false,
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
  })(DumbPinned)
);