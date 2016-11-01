from unittest import TestCase

from context import taggable


class TestTaggableSequence(TestCase):
    def test_constructor_accepts_string(self):
        tagged = taggable.TaggableSequence('Just a string')
        self.assertEqual('Just a string', tagged.sequence)
        self.assertEqual(0, len(tagged.tag_names()))

    def test_constructor_accepts_list(self):
        tagged = taggable.TaggableSequence([1, 2, 3])
        self.assertEqual([1, 2, 3], tagged.sequence)
        self.assertEqual(0, len(tagged.tag_names()))

    def test_iteration(self):
        tagged = taggable.TaggableSequence('tag this string')
        tagged.tag_at(0, 2, 'POS', 'VERB')
        tagged.tag_at(4, 7, 'TOKEN', 'WORD')
        values = [tag.tag for tag in tagged]
        self.assertSequenceEqual(['VERB', 'WORD'], sorted(values))

    def test_len(self):
        tagged = taggable.TaggableSequence([1, 2, 3])
        self.assertEqual(3, len(tagged))

    def test_getitem(self):
        tagged = taggable.TaggableSequence([1, 2, 3])
        self.assertEqual(2, tagged[1])

    def test_tag(self):
        tagged = taggable.TaggableSequence('Run')
        tagged.tag('POS', 'VERB')
        self.assertEqual(['POS'], list(tagged.tag_names()))
        self.assertSequenceEqual([taggable.TaggedSegment(0, 2, 'POS', 'VERB')], tagged.tags('POS'))

    def test_tags_none(self):
        tagged = taggable.TaggableSequence([])
        self.assertIsNone(tagged.tags('TIME'))

    def test_tags_one(self):
        tagged = taggable.TaggableSequence('tag this string')
        tagged.tag_at(0, 2, 'POS', 'VERB')
        self.assertEqual(1, len(tagged.tags('POS')))
        self.assertSequenceEqual(['POS'], list(tagged.tag_names()))

    def test_tags_two(self):
        tagged = taggable.TaggableSequence('tag this string')
        tagged.tag_at(0, 2, 'POS', 'VERB')
        tagged.tag_at(9, 14, 'POS', 'NOUN')
        self.assertEqual(2, len(tagged.tags('POS')))
        self.assertSequenceEqual(['POS'], list(tagged.tag_names()))

    def test_tags_heterogeneous(self):
        tagged = taggable.TaggableSequence('tag this string')
        tagged.tag_at(0, 2, 'POS', 'VERB')
        tagged.tag_at(0, 2, 'SENTIMENT', 'NEUTRAL')
        self.assertEqual(1, len(tagged.tags('POS')))
        self.assertEqual(1, len(tagged.tags('SENTIMENT')))
        self.assertSequenceEqual(['POS', 'SENTIMENT'], sorted(tagged.tag_names()))

    def test_tag_at(self):
        tagged = taggable.TaggableSequence('tag this string')
        tagged.tag_at(0, 2, 'POS', 'VERB')
        self.assertEqual(taggable.TaggedSegment(0, 2, 'POS', 'VERB'), tagged.tags('POS')[0])

    def test_tags_at_single(self):
        tagged = taggable.TaggableSequence('tag this string')
        tagged.tag_at(0, 2, 'POS', 'VERB')
        self.assertEqual(1, len(tagged.tags_at(0)))
        self.assertEqual(taggable.TaggedSegment(0, 2, 'POS', 'VERB'), tagged.tags_at(0)[0])

    def test_tags_at_multiple_overlapping(self):
        tagged = taggable.TaggableSequence('tag this string')
        tagged.tag_at(0, 2, 'POS', 'VERB')
        tagged.tag_at(0, 2, 'TOKEN', 'WORD')
        self.assertEqual(2, len(tagged.tags_at(0)))
        self.assertEqual(
            set([taggable.TaggedSegment(0, 2, 'POS', 'VERB'), taggable.TaggedSegment(0, 2, 'TOKEN', 'WORD')]),
            set(tagged.tags_at(0))
        )

    def test_tags_at_multiple_non_overlapping(self):
        tagged = taggable.TaggableSequence('tag this string')
        tagged.tag_at(0, 2, 'POS', 'VERB')
        tagged.tag_at(4, 7, 'TOKEN', 'WORD')

        self.assertEqual(1, len(tagged.tags_at(0)))
        self.assertEqual(1, len(tagged.tags_at(2)))
        self.assertEqual([taggable.TaggedSegment(0, 2, 'POS', 'VERB')], tagged.tags_at(1))

        self.assertEqual(0, len(tagged.tags_at(3)))

        self.assertEqual(1, len(tagged.tags_at(4)))
        self.assertEqual(1, len(tagged.tags_at(7)))
        self.assertEqual([taggable.TaggedSegment(4, 7, 'TOKEN', 'WORD')], tagged.tags_at(5))

        self.assertEqual(0, len(tagged.tags_at(8)))


if __name__ == '__main__':
    import unittest

    unittest.main()
