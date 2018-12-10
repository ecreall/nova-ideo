import update from 'immutability-helper';
import gql from 'graphql-tag';
import Moment from 'moment';

export const editDeadlineMutation = gql`
  mutation($context: String!, $date: String!) {
    editDeadline(context: $context) {
      root {
        examinationDates {
          start
          end
        }
      }
    }
  }
`;

export default function editDeadline({ mutate }) {
  return ({ context, date }) => {
    const lastDate = context.examinationDates[context.examinationDates.length - 1];
    let newDate = null;
    if (lastDate) {
      newDate = {
        __typename: 'ExaminationDate',
        start: lastDate.start,
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
        editDeadline: {
          __typename: 'EditDeadline',
          root: {
            id: context.id,
            examinationDates: [...context.examinationDates.slice(0, -1), newDate],
            __typename: 'Root'
          }
        }
      },
      updateQueries: {
        SiteData: (prev, { mutationResult }) => {
          const examinationDates = mutationResult.data.editDeadline.root.examinationDates;
          const result = update(prev, {
            root: {
              examinationDates: {
                $set: examinationDates
              }
            }
          });
          return result;
        }
      }
    });
  };
}