/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { connect } from 'react-redux';
import { withApollo } from 'react-apollo';
import { Translate } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import throttle from 'lodash/throttle';

import retext from 'retext';
import Retextkeywords from 'retext-keywords';
import toString from 'nlcst-to-string';

import HasProposals from '../../../../graphql/queries/HasProposals.graphql';
import Button from '../../../styledComponents/Button';
import { openCollaborationRight, closeCollaborationRight } from '../../../../actions/collaborationAppActions';
import { CONTENTS_IDS } from '../../../collaborationApp/collaborationAppRight';

export class DumbSimilarProposalsButton extends React.Component {
  state = {
    hasSimilarProposalsFilter: null,
    hasSimilarProposalsCount: 0
  };

  componentDidMount() {
    this.findSimilarProposals();
  }

  componentDidUpdate() {
    this.findSimilarProposals();
  }

  openSimilarProposals = () => {
    const { hasSimilarProposalsFilter, hasSimilarProposalsCount } = this.state;
    const { openRight, closeRight } = this.props;
    if (hasSimilarProposalsCount > 0) {
      openRight({
        componentId: CONTENTS_IDS.similarProposals,
        props: {
          canExpand: false,
          filter: hasSimilarProposalsFilter,
          generateFilter: true,
          title: <Translate value="forms.similarProposals" count={hasSimilarProposalsCount} />
        }
      });
    } else {
      closeRight({});
    }
  };

  findSimilarProposals = throttle(() => {
    const { text } = this.props;
    if (text) {
      retext()
        .use(Retextkeywords)
        .process(text, this.getSimilarProposals);
    }
  }, 200);

  getSimilarProposals = (err, file) => {
    const { keywords, client, collaborationAppRightOpened } = this.props;
    const { hasSimilarProposalsFilter } = this.state;
    let textkeywords = err
      ? []
      : file.data.keywords
        .filter((keyword) => {
          return keyword.score >= 0.5;
        })
        .map((keyword) => {
          return toString(keyword.matches[0].node);
        });
    textkeywords = [...textkeywords, ...keywords];
    const filterText = textkeywords.join(',');
    const currentFilter = hasSimilarProposalsFilter ? hasSimilarProposalsFilter.text : '';
    if (filterText !== currentFilter && filterText) {
      const filter = {
        text: filterText
      };
      client
        .query({
          query: HasProposals,
          variables: {
            filter: filter
          }
        })
        .then(({ data }) => {
          this.setState({ hasSimilarProposalsFilter: filter, hasSimilarProposalsCount: data.hasProposals }, () => {
            if (collaborationAppRightOpened) {
              this.openSimilarProposals();
            }
          });
        })
        .catch(() => {
          this.setState({ hasSimilarProposalsFilter: filter, hasSimilarProposalsCount: 0 });
        });
    }
  };

  render() {
    const { hasSimilarProposalsCount } = this.state;
    const { theme, defaultContent } = this.props;
    return hasSimilarProposalsCount > 0 ? (
      <Button onClick={this.openSimilarProposals} background={theme.palette.warning[500]}>
        <Translate value="forms.similarProposals" count={hasSimilarProposalsCount} />
      </Button>
    ) : (
      defaultContent
    );
  }
}

const mapStateToProps = (state) => {
  return {
    collaborationAppRightOpened: state.apps.collaborationApp.right.open
  };
};

export const mapDispatchToProps = {
  openRight: openCollaborationRight,
  closeRight: closeCollaborationRight
};

export default withStyles({}, { withTheme: true })(
  withApollo(connect(mapStateToProps, mapDispatchToProps)(DumbSimilarProposalsButton))
);