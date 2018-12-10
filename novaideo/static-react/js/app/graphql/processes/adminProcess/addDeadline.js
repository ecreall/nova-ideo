import update from 'immutability-helper';
import gql from 'graphql-tag';
import Moment from 'moment';

export const addDeadlineMutation = gql`
  mutation($context: String!, $date: String!) {
    addDeadline(context: $context) {
      root {
        examinationDates {
          start
          end
        }
      }
    }
  }
`;

export default function addDeadline({ mutate }) {
  return ({ context, date }) => {
    const lastDate = context.examinationDates[context.examinationDates.length - 1];
    let newDate = null;
    if (lastDate) {
      newDate = {
        __typename: 'ExaminationDate',
        start: lastDate.end,
        end: date.format()
      };
    } else {
      newDate = {
        __typename: 'ExaminationDate',
        start: Moment().format(),
        end: date.format()
      };
    }
    return mutate({
      variables: {
        context: context.oid,
        date: date
      },
      optimisticResponse: {
        __typename: 'Mutation',
        addDeadline: {
          __typename: 'AddDeadline',
          root: {
            id: context.id,
            examinationDates: [...context.examinationDates, newDate],
            __typename: 'Root'
          }
        }
      },
      updateQueries: {
        SiteData: (prev, { mutationResult }) => {
          const examinationDates = mutationResult.data.addDeadline.root.examinationDates;
          return update(prev, {
            root: {
              examinationDates: {
                $set: examinationDates
              }
            }
          });
        }
      }
    });
  };
}