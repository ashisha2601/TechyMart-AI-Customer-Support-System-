"""
Advanced Keyword Management System
Provides comprehensive functions for managing, analyzing, and optimizing keywords
"""

import json
import csv
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter
from keyword_matcher import keyword_matcher

class AdvancedKeywordManager:
    def __init__(self):
        self.keyword_matcher = keyword_matcher
        self.usage_stats = defaultdict(int)
        self.match_history = []
        self.performance_data = {}
        
    # ==================== BASIC MANAGEMENT ====================
    
    def add_keyword(self, keyword: str, category: str, response: str, priority: int = 5, tags: List[str] = None):
        """Enhanced keyword addition with tagging"""
        self.keyword_matcher.add_custom_keyword(keyword, category, response, priority)
        
        # Store metadata
        self.performance_data[keyword] = {
            'created_at': datetime.now().isoformat(),
            'category': category,
            'priority': priority,
            'tags': tags or [],
            'usage_count': 0,
            'success_rate': 0.0
        }
        
        print(f"✅ Added keyword: '{keyword}' (Priority: {priority}, Category: {category})")
    
    def bulk_add_keywords(self, keywords_data: List[Dict]):
        """Add multiple keywords at once"""
        print(f"📦 Adding {len(keywords_data)} keywords in bulk...")
        
        for i, data in enumerate(keywords_data, 1):
            self.add_keyword(
                keyword=data['keyword'],
                category=data['category'],
                response=data['response'],
                priority=data.get('priority', 5),
                tags=data.get('tags', [])
            )
            print(f"   {i}/{len(keywords_data)} - {data['keyword']}")
        
        print(f"🎉 Successfully added {len(keywords_data)} keywords!")
    
    def remove_keyword(self, keyword: str):
        """Remove a keyword from the system"""
        # Remove from exact phrases
        if keyword in self.keyword_matcher.exact_phrases:
            del self.keyword_matcher.exact_phrases[keyword]
            print(f"🗑️ Removed exact phrase: '{keyword}'")
        
        # Remove from patterns (more complex)
        for pattern_name, pattern_data in list(self.keyword_matcher.keyword_patterns.items()):
            if keyword in pattern_data['keywords']:
                pattern_data['keywords'].remove(keyword)
                if not pattern_data['keywords']:  # Remove empty patterns
                    del self.keyword_matcher.keyword_patterns[pattern_name]
                print(f"🗑️ Removed keyword: '{keyword}' from pattern: {pattern_name}")
        
        # Remove metadata
        if keyword in self.performance_data:
            del self.performance_data[keyword]
    
    def update_keyword(self, keyword: str, new_response: str = None, new_priority: int = None, new_category: str = None):
        """Update existing keyword properties"""
        updated = False
        
        # Update in exact phrases
        if keyword in self.keyword_matcher.exact_phrases:
            if new_response:
                self.keyword_matcher.exact_phrases[keyword]['response'] = new_response
                updated = True
            if new_category:
                self.keyword_matcher.exact_phrases[keyword]['category'] = new_category
                updated = True
        
        # Update metadata
        if keyword in self.performance_data:
            if new_priority:
                self.performance_data[keyword]['priority'] = new_priority
            if new_category:
                self.performance_data[keyword]['category'] = new_category
        
        if updated:
            print(f"📝 Updated keyword: '{keyword}'")
        else:
            print(f"❌ Keyword '{keyword}' not found")
    
    # ==================== SEARCH & DISCOVERY ====================
    
    def search_keywords(self, query: str, search_in: str = 'all') -> List[Dict]:
        """Search for keywords by text, category, or response"""
        results = []
        query_lower = query.lower()
        
        # Search exact phrases
        for keyword, data in self.keyword_matcher.exact_phrases.items():
            match = False
            
            if search_in in ['all', 'keyword'] and query_lower in keyword.lower():
                match = True
            elif search_in in ['all', 'category'] and query_lower in data.get('category', '').lower():
                match = True
            elif search_in in ['all', 'response'] and data.get('response') and query_lower in data['response'].lower():
                match = True
            
            if match:
                results.append({
                    'keyword': keyword,
                    'type': 'exact_phrase',
                    'category': data.get('category', 'unknown'),
                    'response': data.get('response', 'N/A')[:100] + '...' if data.get('response') else 'N/A',
                    'confidence': data.get('confidence', 0)
                })
        
        return results
    
    def list_keywords_by_category(self, category: str = None) -> Dict[str, List]:
        """List all keywords organized by category"""
        categories = defaultdict(list)
        
        # From exact phrases
        for keyword, data in self.keyword_matcher.exact_phrases.items():
            cat = data.get('category', 'uncategorized')
            if not category or cat == category:
                categories[cat].append({
                    'keyword': keyword,
                    'type': 'exact_phrase',
                    'priority': data.get('confidence', 0) * 10,
                    'response_length': len(data.get('response', '') or '')
                })
        
        # From patterns
        for pattern_name, pattern_data in self.keyword_matcher.keyword_patterns.items():
            cat = pattern_name.split('_')[0] if '_' in pattern_name else 'general'
            if not category or cat == category:
                for kw in pattern_data['keywords']:
                    categories[cat].append({
                        'keyword': kw,
                        'type': 'pattern',
                        'priority': pattern_data['priority'],
                        'pattern': pattern_name
                    })
        
        return dict(categories)
    
    def find_duplicate_keywords(self) -> List[Dict]:
        """Find potential duplicate or similar keywords"""
        all_keywords = []
        
        # Collect all keywords
        for keyword in self.keyword_matcher.exact_phrases.keys():
            all_keywords.append(keyword)
        
        for pattern_data in self.keyword_matcher.keyword_patterns.values():
            all_keywords.extend(pattern_data['keywords'])
        
        # Find duplicates and similar ones
        duplicates = []
        for i, kw1 in enumerate(all_keywords):
            for j, kw2 in enumerate(all_keywords[i+1:], i+1):
                if kw1 == kw2:
                    duplicates.append({'type': 'exact_duplicate', 'keyword1': kw1, 'keyword2': kw2})
                elif self._are_similar(kw1, kw2):
                    duplicates.append({'type': 'similar', 'keyword1': kw1, 'keyword2': kw2})
        
        return duplicates
    
    def _are_similar(self, kw1: str, kw2: str, threshold: float = 0.8) -> bool:
        """Check if two keywords are similar using simple string similarity"""
        if len(kw1) < 3 or len(kw2) < 3:
            return False
        
        # Simple character overlap ratio
        set1, set2 = set(kw1.lower()), set(kw2.lower())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union > threshold if union > 0 else False
    
    # ==================== ANALYTICS & OPTIMIZATION ====================
    
    def track_keyword_usage(self, keyword: str, user_message: str, success: bool = True):
        """Track how often keywords are used and their success rate"""
        self.usage_stats[keyword] += 1
        
        # Store match history
        self.match_history.append({
            'keyword': keyword,
            'user_message': user_message,
            'timestamp': datetime.now().isoformat(),
            'success': success
        })
        
        # Update performance data
        if keyword in self.performance_data:
            self.performance_data[keyword]['usage_count'] += 1
            
            # Calculate success rate
            keyword_matches = [m for m in self.match_history if m['keyword'] == keyword]
            successful = sum(1 for m in keyword_matches if m['success'])
            self.performance_data[keyword]['success_rate'] = successful / len(keyword_matches)
    
    def get_usage_statistics(self, top_n: int = 10) -> Dict:
        """Get comprehensive usage statistics"""
        stats = {
            'total_keywords': len(self.keyword_matcher.exact_phrases) + sum(len(p['keywords']) for p in self.keyword_matcher.keyword_patterns.values()),
            'total_matches': len(self.match_history),
            'top_keywords': dict(Counter(self.usage_stats).most_common(top_n)),
            'categories': self._get_category_stats(),
            'performance_summary': self._get_performance_summary()
        }
        
        return stats
    
    def _get_category_stats(self) -> Dict:
        """Get statistics by category"""
        category_stats = defaultdict(int)
        
        for data in self.performance_data.values():
            category_stats[data['category']] += data['usage_count']
        
        return dict(category_stats)
    
    def _get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if not self.performance_data:
            return {}
        
        success_rates = [data['success_rate'] for data in self.performance_data.values()]
        usage_counts = [data['usage_count'] for data in self.performance_data.values()]
        
        return {
            'avg_success_rate': sum(success_rates) / len(success_rates),
            'avg_usage_per_keyword': sum(usage_counts) / len(usage_counts),
            'most_successful': max(self.performance_data.items(), key=lambda x: x[1]['success_rate'])[0],
            'most_used': max(self.performance_data.items(), key=lambda x: x[1]['usage_count'])[0]
        }
    
    def get_low_performing_keywords(self, min_usage: int = 5, max_success_rate: float = 0.5) -> List[Dict]:
        """Find keywords that might need improvement"""
        low_performers = []
        
        for keyword, data in self.performance_data.items():
            if data['usage_count'] >= min_usage and data['success_rate'] <= max_success_rate:
                low_performers.append({
                    'keyword': keyword,
                    'usage_count': data['usage_count'],
                    'success_rate': data['success_rate'],
                    'category': data['category']
                })
        
        return sorted(low_performers, key=lambda x: x['success_rate'])
    
    def suggest_keyword_improvements(self, keyword: str) -> Dict:
        """Analyze keyword and suggest improvements"""
        if keyword not in self.performance_data:
            return {'error': 'Keyword not found'}
        
        data = self.performance_data[keyword]
        suggestions = []
        
        # Analyze usage patterns
        keyword_matches = [m for m in self.match_history if m['keyword'] == keyword]
        failed_matches = [m for m in keyword_matches if not m['success']]
        
        if data['success_rate'] < 0.7:
            suggestions.append("Consider improving the response - success rate is low")
        
        if data['usage_count'] < 2:
            suggestions.append("Keyword rarely used - consider promoting or removing")
        
        if len(failed_matches) > 0:
            common_failures = Counter(m['user_message'] for m in failed_matches)
            suggestions.append(f"Common failed queries: {list(common_failures.keys())[:3]}")
        
        return {
            'keyword': keyword,
            'current_performance': data,
            'suggestions': suggestions,
            'similar_successful_keywords': self._find_similar_successful_keywords(keyword)
        }
    
    def _find_similar_successful_keywords(self, keyword: str) -> List[str]:
        """Find similar keywords that perform well"""
        similar = []
        
        for other_keyword, data in self.performance_data.items():
            if (other_keyword != keyword and 
                data['success_rate'] > 0.8 and 
                self._are_similar(keyword, other_keyword, 0.6)):
                similar.append(other_keyword)
        
        return similar[:3]
    
    # ==================== IMPORT/EXPORT ====================
    
    def export_keywords_to_json(self, filename: str = None):
        """Export all keywords to JSON file"""
        if not filename:
            filename = f"keywords_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            'exact_phrases': self.keyword_matcher.exact_phrases,
            'keyword_patterns': self.keyword_matcher.keyword_patterns,
            'performance_data': self.performance_data,
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Exported keywords to: {filename}")
        return filename
    
    def import_keywords_from_json(self, filename: str):
        """Import keywords from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Import exact phrases
            if 'exact_phrases' in data:
                self.keyword_matcher.exact_phrases.update(data['exact_phrases'])
                print(f"✅ Imported {len(data['exact_phrases'])} exact phrases")
            
            # Import patterns
            if 'keyword_patterns' in data:
                self.keyword_matcher.keyword_patterns.update(data['keyword_patterns'])
                print(f"✅ Imported {len(data['keyword_patterns'])} patterns")
            
            # Import performance data
            if 'performance_data' in data:
                self.performance_data.update(data['performance_data'])
                print(f"✅ Imported performance data for {len(data['performance_data'])} keywords")
            
            print(f"🎉 Successfully imported from: {filename}")
            
        except Exception as e:
            print(f"❌ Error importing: {e}")
    
    def export_to_csv(self, filename: str = None):
        """Export keywords to CSV for easy editing"""
        if not filename:
            filename = f"keywords_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Keyword', 'Category', 'Response', 'Priority', 'Usage Count', 'Success Rate'])
            
            for keyword, data in self.keyword_matcher.exact_phrases.items():
                perf_data = self.performance_data.get(keyword, {})
                writer.writerow([
                    keyword,
                    data.get('category', 'unknown'),
                    (data.get('response') or '')[:200],  # Truncate long responses
                    perf_data.get('priority', 'N/A'),
                    perf_data.get('usage_count', 0),
                    f"{perf_data.get('success_rate', 0):.2f}"
                ])
        
        print(f"📊 Exported to CSV: {filename}")
        return filename
    
    def import_from_csv(self, filename: str):
        """Import keywords from CSV file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                
                for row in reader:
                    if row['Keyword'] and row['Response']:
                        self.add_keyword(
                            keyword=row['Keyword'],
                            category=row['Category'] or 'imported',
                            response=row['Response'],
                            priority=int(row['Priority']) if row['Priority'].isdigit() else 5
                        )
                        count += 1
                
                print(f"✅ Imported {count} keywords from CSV")
                
        except Exception as e:
            print(f"❌ Error importing CSV: {e}")
    
    # ==================== AUTOMATION ====================
    
    def auto_optimize_keywords(self):
        """Automatically optimize keyword priorities based on performance"""
        optimized = 0
        
        for keyword, data in self.performance_data.items():
            new_priority = data['priority']
            
            # Increase priority for high-performing keywords
            if data['success_rate'] > 0.9 and data['usage_count'] > 10:
                new_priority = min(10, data['priority'] + 1)
            
            # Decrease priority for low-performing keywords
            elif data['success_rate'] < 0.5 and data['usage_count'] > 5:
                new_priority = max(1, data['priority'] - 1)
            
            if new_priority != data['priority']:
                self.update_keyword(keyword, new_priority=new_priority)
                optimized += 1
        
        print(f"🔧 Auto-optimized {optimized} keywords")
        return optimized
    
    def generate_keyword_suggestions(self, user_messages: List[str]) -> List[Dict]:
        """Analyze user messages and suggest new keywords"""
        suggestions = []
        
        # Simple frequency analysis
        word_freq = Counter()
        phrase_freq = Counter()
        
        for message in user_messages:
            words = re.findall(r'\b\w+\b', message.lower())
            word_freq.update(words)
            
            # Extract 2-3 word phrases
            for i in range(len(words) - 1):
                phrase = ' '.join(words[i:i+2])
                phrase_freq.update([phrase])
                
                if i < len(words) - 2:
                    phrase3 = ' '.join(words[i:i+3])
                    phrase_freq.update([phrase3])
        
        # Suggest top phrases not already in keywords
        existing_keywords = set(self.keyword_matcher.exact_phrases.keys())
        
        for phrase, count in phrase_freq.most_common(20):
            if (count >= 3 and 
                phrase not in existing_keywords and 
                len(phrase) > 5 and 
                not any(word in phrase for word in ['the', 'and', 'or', 'but', 'is', 'are'])):
                
                suggestions.append({
                    'suggested_keyword': phrase,
                    'frequency': count,
                    'confidence': min(count / len(user_messages), 1.0),
                    'category': 'auto_suggested'
                })
        
        return suggestions[:10]
    
    # ==================== TESTING & VALIDATION ====================
    
    def test_keyword_coverage(self, test_messages: List[str]) -> Dict:
        """Test how well keywords cover a set of test messages"""
        results = {
            'total_messages': len(test_messages),
            'matched': 0,
            'unmatched': [],
            'matches': []
        }
        
        for message in test_messages:
            response = self.keyword_matcher.generate_keyword_response(message)
            
            if response:
                results['matched'] += 1
                results['matches'].append({
                    'message': message,
                    'matched_keyword': response.get('method', 'unknown'),
                    'confidence': response.get('confidence', 0)
                })
            else:
                results['unmatched'].append(message)
        
        results['coverage_rate'] = results['matched'] / results['total_messages']
        return results
    
    def validate_all_keywords(self) -> List[Dict]:
        """Validate all keywords for potential issues"""
        issues = []
        
        for keyword, data in self.keyword_matcher.exact_phrases.items():
            # Check for empty responses
            if not data.get('response'):
                issues.append({
                    'keyword': keyword,
                    'issue': 'empty_response',
                    'severity': 'high'
                })
            
            # Check for very long responses
            elif len(data.get('response', '')) > 500:
                issues.append({
                    'keyword': keyword,
                    'issue': 'response_too_long',
                    'severity': 'medium'
                })
            
            # Check for missing categories
            if not data.get('category'):
                issues.append({
                    'keyword': keyword,
                    'issue': 'missing_category',
                    'severity': 'low'
                })
        
        return issues

# Global advanced keyword manager
keyword_manager = AdvancedKeywordManager()
