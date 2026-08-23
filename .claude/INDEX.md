# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (255)

```
 10441  GET              /                                                dashboard
 15331  GET              /api/abo/status                                  api_abo_status
 10540  GET              /api/active-recordings                           api_active_recordings
 15406  GET              /api/activity-pulse                              api_activity_pulse
 14759  GET              /api/ai-log                                      api_ai_log
 10938  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15166  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 22750  GET/POST         /api/audio/config                                api_audio_config
 22780  POST             /api/audio/testtone                              api_audio_testtone
 15272  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15296  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15300  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12216  GET              /api/automation/status                           api_automation_status
 12238  POST             /api/automation/toggle                           api_automation_toggle
 13964  GET              /api/azrael/agents                               api_azrael_agents
 12119  POST             /api/azrael/ask                                  api_azrael_ask
 22986  GET/POST         /api/azrael/context                              api_azrael_context
 13591  GET              /api/azrael/core                                 api_azrael_core
 23120  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23110  GET              /api/azrael/live_status                          api_azrael_live_status
 23128  POST             /api/azrael/live_test                            api_azrael_live_test
 13973  GET              /api/azrael/memories                             api_azrael_memories
 23176  POST             /api/azrael/persona                              api_azrael_persona_set
 23167  GET              /api/azrael/personas                             api_azrael_personas
 23204  GET              /api/azrael/piper_status                         api_azrael_piper_status
 22959  POST             /api/azrael/react                                api_azrael_react
 22995  GET              /api/azrael/reaction                             api_azrael_reaction
 23147  GET              /api/azrael/reactions                            api_azrael_reactions
 23197  GET              /api/azrael/transcript                           api_azrael_transcript
 23082  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23057  GET              /api/azrael/voices                               api_azrael_voices
 23221  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11033  GET              /api/backoff-watch                               api_backoff_watch
 14530  POST             /api/backup/run                                  api_backup_run
 14496  GET              /api/backup/status                               api_backup_status
 14485  POST             /api/backup/system                               api_backup_system
 15238  GET              /api/bandwidth/live                              api_bandwidth_live
 15151  GET              /api/bookmarks                                   api_bookmarks_list
 11296  GET              /api/brain                                       api_brain
 11233  GET              /api/brain/alarms                                api_brain_alarms
 11218  GET              /api/brain/creator                               api_brain_creator
 11195  GET              /api/brain/graph                                 api_brain_graph
 11256  GET              /api/brain/growth                                api_brain_growth
 10037  GET              /api/brain/health                                api_brain_health
 23702  GET              /api/channel/categories                          api_channel_categories
 23708  POST             /api/channel/set                                 api_channel_set
 23518  GET              /api/channels/status                             api_channels_status
 22351  POST             /api/chat/send                                   api_chat_send
 14231  GET              /api/chat/send_status                            api_chat_send_status
 10521  GET              /api/checks                                      api_checks
 23023  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23006  GET              /api/clips                                       api_clips
 23039  POST/DELETE      /api/clips/clear                                 api_clips_clear
 22625  GET              /api/cohost                                      api_cohost
 22637  POST             /api/cohost/config                               api_cohost_config
 15970  GET              /api/community/stats                             api_community_stats
 24702  POST             /api/config/restore                              api_config_restore
 24687  GET              /api/config/snapshot                             api_config_snapshot
 15429  GET              /api/cookies/age                                 api_cookies_age
 10588  GET              /api/cookies/health                              api_cookies_health
 10595  POST             /api/cookies/update                              api_cookies_update
 24653  GET              /api/data/export                                 api_data_export
 16480  GET              /api/db/export                                   api_db_export
 16507  POST             /api/db/import                                   api_db_import
 16467  GET              /api/db/summary                                  api_db_summary
 22551  GET              /api/debug/threads                               api_debug_threads
 25588  GET              /api/defense/attacks                             api_defense_attacks
 25555  GET              /api/defense/crowdsec                            api_defense_crowdsec
 25573  GET              /api/defense/fail2ban                            api_defense_fail2ban
 25279  GET              /api/defense/overview                            api_defense_overview
 14592  POST             /api/discord/announce                            api_discord_announce
 14320  GET              /api/discord/clips_week                          api_discord_clips_week
 14536  GET              /api/discord/community                           api_discord_community
 14259  GET              /api/discord/invite                              api_discord_invite
 13722  GET              /api/discord/overview                            api_discord_overview
 13808  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16047  POST             /api/donations/add                               api_donations_add
 16080  GET              /api/donations/manual                            api_donations_manual
 16088  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 15983  POST             /api/donations/reset                             api_donations_reset
 16104  GET              /api/donations/summary                           api_donations_summary
 15220  GET              /api/events                                      api_events
 14367  GET              /api/events/stream                               api_events_stream
 17135  GET              /api/evolution/changelog                         api_evolution_changelog
 17120  GET              /api/evolution/history                           api_evolution_history
 17060  GET              /api/evolution/learned                           api_evolution_learned
 17082  GET              /api/evolution/proposals                         api_evolution_proposals
 17103  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17050  POST             /api/evolution/run                               api_evolution_run
 17150  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17015  GET              /api/evolution/status                            api_evolution_status
 16314  GET              /api/finanzamt/entries                           api_finanzamt_entries
 16334  POST             /api/finanzamt/entry                             api_finanzamt_add
 16361  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15233  GET              /api/forecast/storage                            api_forecast_storage
 12254  GET              /api/freeai/status                               api_freeai_status
 13664  GET              /api/health                                      api_health
 15251  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15247  GET              /api/heatmap/recordings                          api_heatmap_recordings
 22674  GET              /api/highlights                                  api_highlights
 22686  POST             /api/highlights/config                           api_highlights_config
 23559  GET              /api/kick/channel                                api_kick_channel
 23580  POST             /api/kick/channel                                api_kick_channel_set
 13391  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13459  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13437  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13376  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13416  GET              /api/kick/oauth/status                           api_kick_oauth_status
 22798  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 22867  POST             /api/kickmod/config                              api_kickmod_config
 22912  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 22926  GET              /api/kickmod/learned                             api_kickmod_learned
 22953  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 22933  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 23264  POST             /api/kickmod/say                                 api_kickmod_say
 23240  POST             /api/kickmod/start                               api_kickmod_start
 22838  GET              /api/kickmod/status                              api_kickmod_status
 23251  POST             /api/kickmod/stop                                api_kickmod_stop
 10373  POST             /api/login                                       dashboard_login_submit
 15955  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12669  POST             /api/marketing/config                            api_marketing_config
 12694  GET              /api/marketing/preview                           api_marketing_preview
 12704  POST             /api/marketing/send-now                          api_marketing_send_now
 12643  GET              /api/marketing/status                            api_marketing_status
 12661  POST             /api/marketing/toggle                            api_marketing_toggle
 22701  GET              /api/moderation/feed                             api_moderation_feed
 13222  POST             /api/news/config                                 api_news_config
 13188  GET              /api/news/creators                               api_news_creators
 13199  POST             /api/news/creators/generate                      api_news_creators_generate
 13264  POST             /api/news/generate-now                           api_news_generate_now
 13259  GET              /api/news/items                                  api_news_items
 13250  GET              /api/news/preview                                api_news_preview
 13169  GET              /api/news/status                                 api_news_status
 13214  POST             /api/news/toggle                                 api_news_toggle
 15812  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14196  GET              /api/notify/status                               api_notify_status
 14207  POST             /api/notify/test                                 api_notify_test
 14182  GET              /api/ops/audit                                   api_ops_audit
 15883  GET              /api/ops/db-stats                                api_ops_db_stats
 15911  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 13988  GET              /api/ops/errors                                  api_ops_errors
 15832  GET              /api/ops/healthcheck                             api_ops_healthcheck
 16562  GET              /api/ops/log-tail                                api_ops_log_tail
 12099  GET              /api/ops/logtail                                 api_ops_logtail
 13929  GET              /api/ops/metrics                                 api_ops_metrics
 13912  GET              /api/ops/resource_history                        api_ops_resource_history
 16536  GET              /api/ops/version                                 api_ops_version
 10791  GET              /api/outcomes                                    api_outcomes
 24183  POST             /api/overlay/config                              api_overlay_config
 24170  POST             /api/overlay/event                               api_overlay_event
 24075  GET              /api/overlay/state                               api_overlay_state
 10824  GET              /api/profile/<username>                          api_profile
 15437  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15259  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15385  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15362  GET              /api/proxy/trend                                 api_proxy_trend
 13143  GET              /api/public/stats                                api_public_stats
 10475  GET              /api/pulse                                       api_pulse
 14783  GET              /api/recording-attempts                          api_recording_attempts
 22286  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 22264  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 22305  POST             /api/restream/<int:rid>/start                    api_restream_start
 22572  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24037  GET              /api/restream/chatfeed                           api_restream_chatfeed
 22240  POST             /api/restream/create                             api_restream_create
 13467  GET              /api/restream/deck                               api_restream_deck
 12190  GET              /api/restream/health                             api_restream_health
 24059  POST             /api/restream/layout                             api_restream_layout
 22213  GET              /api/restream/list                               api_restream_list
 12163  POST             /api/restream/report                             api_restream_report
 22585  POST             /api/restream/start_all                          api_restream_start_all
 22611  POST             /api/restream/stop_all                           api_restream_stop_all
 12417  GET              /api/restream/testpush                           api_testpush_status
 12442  POST             /api/restream/testpush                           api_testpush_run
 16220  GET              /api/restream/verify                             api_restream_verify
 14298  GET              /api/retention/preview                           api_retention_preview
 14307  POST             /api/retention/run                               api_retention_run
 24768  POST             /api/schedule/add                                api_schedule_add
 24758  GET              /api/schedule/list                               api_schedule_list
 24793  POST             /api/schedule/remove                             api_schedule_remove
 15136  GET              /api/search                                      api_search
 25326  GET              /api/selftest                                    api_selftest
 22322  GET              /api/shield/stats                                api_shield_stats
 10494  GET              /api/stats                                       api_stats
 15400  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15327  GET              /api/stats/tiktok-status                         api_tiktok_status
 24733  GET              /api/stats/timeline                              api_stats_timeline
 10562  GET              /api/storage                                     api_storage
 10569  POST             /api/storage/cleanup                             api_storage_cleanup
 15313  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12140  GET              /api/stream/timeline                             api_stream_timeline
 13796  GET              /api/stream/transcript                           api_stream_transcript
 24401  GET              /api/streamer/compare                            api_streamer_compare
 24600  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14272  GET              /api/streamer/detail                             api_streamer_detail
 24625  GET              /api/streamer/digest/<username>                  api_streamer_digest
 24505  GET              /api/streamer/dormant                            api_streamer_dormant
 24581  GET              /api/streamer/exists/<username>                  api_streamer_exists
 24460  GET              /api/streamer/journal/<username>                 api_streamer_journal
 24425  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 24485  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13631  GET              /api/streamers/wall                              api_streamers_wall
 10711  GET              /api/summary/preview                             api_summary_preview
 14848  GET              /api/system                                      api_system
 16168  GET              /api/system/check_timing                         api_check_timing
 16448  GET              /api/system/config_drift                         api_config_drift
 13832  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14043  GET              /api/system/preflight                            api_system_preflight
 14169  GET              /api/system/preflight_history                    api_system_preflight_history
 14432  GET              /api/system/resilience                           api_system_resilience
 15171  GET              /api/tags                                        api_tags_list
 10535  GET              /api/top                                         api_top
 12073  GET              /api/trackings                                   api_trackings
 15701  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 15734  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15207  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 15763  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15193  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 14622  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 14669  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 14698  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 14680  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10728  POST             /api/trackings/bulk                              api_trackings_bulk
 14637  GET              /api/trackings/export                            api_trackings_export
 15175  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15475  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11088  GET              /api/trend-7d                                    api_trend_7d
 23071  GET              /api/tts/<fn>                                    api_tts_file
 12297  POST             /api/tunnel/set                                  api_tunnel_set
 12276  GET              /api/tunnel/status                               api_tunnel_status
 12308  POST             /api/tunnel/test                                 api_tunnel_test
 12289  POST             /api/tunnel/toggle                               api_tunnel_toggle
 16420  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16397  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16379  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 24211  GET              /api/upload_window                               api_upload_window
 10805  GET              /api/userstats                                   api_userstats
 13275  GET              /api/version                                     api_version
 16276  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16297  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16261  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16245  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 29006  GET              /api/youtube/sendrate                            api_youtube_sendrate
 14821  GET              /archive/<int:eid>/download                      archive_download
 14878  GET              /download/<int:recording_id>                     download
 14744  GET              /health                                          health
 22520  GET              /healthz                                         healthz
 10362  GET              /login                                           dashboard_login_page
 10396  GET              /logout                                          dashboard_logout
 10403  GET              /manifest.webmanifest                            pwa_manifest
 13860  GET              /metrics                                         api_prometheus_metrics
 24020  GET              /overlay                                         overlay_page
 10427  GET              /pwa-icon-<variant>.png                          pwa_icon
 10413  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (90)

```
   966  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   706  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   837  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   817  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   855  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   779  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   319  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   330  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   340  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   363  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   370  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   381  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   514  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   612  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1204  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1236  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   303  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   919  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   899  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1072  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1120  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1171  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1030  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   874  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   814  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   896  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   924  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   935  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   801  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   863  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   850  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   831  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   476  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   471  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   519  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   402  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   729  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   493  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   456  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   429  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   573  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   662  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   568  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   501  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   281  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   746  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   369  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   624  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   779  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   764  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   325  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   563  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   549  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   532  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   589  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   682  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   578  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 26031  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 26490  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 26122  /assign_role            Rolle/Gruppe einem Mitglied geben
 26168  /ban                    Mitglied bannen
 26822  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 26746  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 26786  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 26771  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 26613  /clips                  Letzte Highlight-Clips eines Users
 26083  /create_category        Kategorie anlegen
 26052  /create_channel         Text-Channel anlegen (optional in Kategorie)
 26111  /create_group           Nutzergruppe (= Rolle) anlegen
 26094  /create_role            Rolle / Nutzergruppe anlegen
 26068  /create_voice           Voice-Channel anlegen
 26404  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 26520  /event                  Community-Event ankündigen (Admin) — mit Countdown
 26563  /events                 Kommende Community-Events anzeigen
 26659  /follow                 Bei Live-Gang eines Streamers gepingt werden
 26643  /help                   Alle Bot-Befehle anzeigen
 26157  /kick                   Mitglied kicken
 26386  /leaderboard            Top-10 der Community nach XP
 26599  /livenow                Welche getrackten User sind gerade live
 26629  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 26460  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 26192  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 26372  /rank                   Dein Level und Rang anzeigen
 26586  /recstatus              Aktuell laufende Aufnahmen
 26133  /remove_role            Rolle/Gruppe entfernen
 26045  /restream_status        Restream-Status
 26144  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 26337  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 26355  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 26685  /stats                  Statistik zu einem getrackten Streamer
 25957  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 26981  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 26878  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 26854  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 26179  /timeout                Mitglied stummschalten (Minuten)
 26757  /topstreamers           Rangliste der Streamer nach Aufnahmen
 25987  /track                  TikTok-User tracken
 25971  /tracklist              Getrackte TikTok-User dieses Servers
 26674  /unfollow               Live-Pings für einen Streamer abbestellen
 26020  /untrack                TikTok-User nicht mehr tracken
 26707  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 26731  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 27465  on_member_join
 27427  on_message
 27068  on_raw_reaction_add
 27500  on_ready
```

## Top-Level-Symbole in bot_v37.py (551 Funktionen, 2 Klassen)

```
  2372-2373   _abo_key
  2393-2411   _abo_probe_dump
 24868-24878  _active_recorder_sync
 19526-19533  _ad_allowlist
 20639-20645  _agent_for
 24880-24898  _ai_calls_total_sync
 20648-20664  _ai_telemetry
 21146-21164  _alert
 27613-27663  _alert_monitor_loop
 28037-28099  _announce_loop
  3314-3317   _anthropic_key
  3324-3326   _anthropic_model
 10165-10168  _arg_int
  2364-2369   _as_dict
 17732-17737  _audio_cfg
 21300-21322  _audio_tap_cmd
 10298-10309  _auth_cookie
 10265-10294  _auth_guard
  1520-1525   _auto_on
 22189-22207  _auto_restream_loop
 29167-29182  _azrael_broadcast_reply
 29067-29089  _azrael_chat_reply
 29050-29064  _azrael_chat_should_reply
 12869-12887  _azrael_creator_take
 29095-29097  _azrael_gate_cfg
 20669-20683  _azrael_live_state
 23919-23933  _azrael_overlay_state
 21029-21083  _azrael_proactive_loop
 20488-20544  _azrael_reaction_to_chats
 29100-29107  _azrael_reply_all_chats
 29037-29047  _azrael_self_names
 29135-29164  _azrael_send_to
 20686-20707  _azrael_system
 27777-27780  _backup_active
 27858-27871  _backup_loop
 19414-19415  _badwords_path
 27578-27587  _brain_growth_loop
 11164-11191  _brain_growth_snapshot
  2300-2320   _brain_hint_delay
 11156-11158  _brain_history_for
  6736-6764   _brain_notify
 11133-11154  _brain_record
 11160-11162  _brain_stream_recent
 14346-14363  _browser_push
  6780-6867   _build_daily_summary
  2803-2983   _build_native_cmd
 18080-18267  _build_restream_cmd
  3027-3060   _build_ytdlp_cmd
 24820-24827  _cached_probe
  5558-5585   _can_stop_tracking
  1700-1722   _capture_set_cookies
 15523-15526  _cfg_get
 15529-15531  _cfg_set
 23663-23698  _channel_set_all
 17330-17333  _chat_connected
 17336-17352  _chat_disconnected
  8762-8773   _chat_is_forum
 17372-17374  _chat_sanitize
 17376-17385  _chat_src_ok
 17315-17327  _chat_stat
 17355-17358  _chat_stats_snapshot
  3589-3600   _check_ai_alive_sync
  3603-3615   _check_ai_models_sync
 24829-24842  _check_redis_alive_sync
 24844-24864  _check_redis_version_sync
 11763-11806  _classify_pool_anonymity
 11809-11826  _classify_pool_anonymity_bg
   754-758    _claude_chat_sync_metered
 10190-10197  _client_ip
 28131-28158  _clip_prune
 28161-28171  _clip_recfile_for
 28687-28693  _clip_should_velocity
 28212-28294  _clip_to_discord
  3487-3496   _close_ai_session
 29211-29226  _cohost_broadcast
 29193-29197  _cohost_cfg
 29252-29264  _cohost_fire_highlight
 29200-29208  _cohost_gate
 29229-29249  _cohost_highlight
 28343-28377  _community_events_loop
 10987-10989  _conv_messages
  7160-7200   _cookie_alarm_loop
  1772-1776   _cookie_autorefresh_info
  1677-1681   _cookie_header
 14396-14428  _cpu_load_snapshot
  3797-3809   _create_index_safe
 12837-12852  _creator_activity
 12893-12916  _creator_dossier_generate
 12855-12866  _creator_facts_line
 25081-25187  _crowdsec_status
 25047-25078  _crowdsec_via_lapi
 24912-24930  _cscli_bin
 24936-24949  _cscli_path
  7053-7078   _daily_summary_loop
 24967-24984  _darf_journal_lesen
 27590-27610  _db_maintenance_loop
  7025-7050   _db_vacuum_loop
 19549-19573  _detect_foreign_ad
  1277-1288   _diag_path_owner
 20935-20979  _director_finalize
 21746-21753  _director_for
 20884-20932  _director_mark
 28581-28616  _disc_automod_check
 28554-28560  _disc_state_get
 28563-28570  _disc_state_set
 25630-25643  _discord_guild_filesize_bytes
 25829-25838  _discord_invite
 28515-28551  _discord_live_thread
 21086-21098  _discord_notify
 25730-25755  _discord_ops_alert
 28413-28511  _discord_post_user
 25894-27575  _discord_run_once
 25768-25826  _discord_start
 28102-28108  _discord_stop
 25651-25653  _discord_upload_limit_label
 25646-25648  _discord_upload_limit_mb
  7081-7155   _disk_alarm_loop
 30480-30529  _disk_autoclean
 30532-30545  _disk_guard_loop
 30472-30477  _disk_pct
 23976-23979  _donations_unknown_count
 17689-17691  _drawtext_chain
 14975-14977  _dump_all_threads
 11688-11752  _enrich_proxies_with_geo
  1917-1961   _ensure_cookie_file_netscape
 25841-25891  _ensure_discord_invite
 28308-28340  _ensure_error_channel
 11931-11968  _ensure_proxy_ready
  8775-8798   _ensure_topic
   637-639    _env_int
   642-644    _env_int_range
 28380-28410  _error_channel_loop
 21130-21143  _event_webhook
 16623-16629  _evo_build_dir
 16632-16639  _evo_version
 16915-16996  _evolution_cycle
 16648-16668  _evolution_llm_note
 16999-17009  _evolution_loop
 16671-16912  _evolution_write_build
  6178-6212   _extract_file_payload
  2049-2051   _extract_urls_from_streamurl_node
 24952-24959  _f2b_sudo_hint
 21166-21168  _faster_whisper_available
 19438-19450  _fetch_ldnoobw_de
 11577-11595  _fetch_proxy_list
 21580-21608  _fetch_tiktok_room_id
   688-691    _ff_cmd
 15646-15659  _ffmpeg_version_str
 17852-17857  _find_chromium
  3020-3024   _find_external_recorder
  2054-2056   _find_stream_urls
 15574-15599  _fire_webhooks
  7936-7945   _fork_safe
   769-778    _freeai_chat_sync_metered
 25002-25044  _geo_lookup_ips
  3476-3485   _get_ai_session
  7770-7810   _get_live_info
  2590-2597   _get_resolve_semaphore
  8124-8489   _handle_single_tracking
 30324-30326  _hb
 30329-30346  _hb_while
 17390-17392  _highlight_cfg
 17395-17424  _highlight_observe
 17860-17865  _htmlov_screenshot_cmd
 21324-21334  _httpx_proxy
 15607-15619  _in_quiet_hours
 31313-31344  _install_fast_eventloop
 10060-10114  _install_fast_json
 14980-14996  _install_faulthandler
 22432-22441  _intel_ensure_schema
 22479-22510  _intel_index_loop
 22453-22463  _intel_index_one
 22444-22450  _intel_semantic
  5547-5556   _is_authorized
  8054-8060   _is_dead
  2039-2041   _is_hevc
 24987-24993  _is_private_ip
  1423-1430   _is_process_running
  6766-6777   _is_quiet_hours
  1085-1094   _is_upload_window
 10149-10162  _json_error_handler
  6983-7013   _kick_broadcaster_id
 12343-12362  _kick_channel_live
  6900-6942   _kick_follower_count
 13354-13367  _kick_oauth_exchange
 13370-13372  _kick_oauth_page
 13313-13317  _kick_redirect_public
 13304-13310  _kick_redirect_source
 13290-13301  _kick_redirect_uri
  6885-6887   _kick_slug
 13320-13351  _kick_user_token
  3846-3849   _kind_from_filename
 15636-15641  _latest_popularity
 19460-19466  _learned_load
 19457-19458  _learned_path
 19468-19476  _learned_save
 21961-21991  _live_react_loop
 21757-21950  _live_react_worker
 20547-20558  _live_transcript_push
 21952-21959  _live_users
 20982-21026  _living_title_loop
 19417-19425  _load_banned_words_file
  1598-1671   _load_cookies_dict
 27783-27855  _local_backup_scan
 10131-10145  _log_5xx
 18275-18279  _looks_like_codec_err
 18270-18272  _looks_like_source_expired
  8017-8047   _loop_fehler
 15000-15009  _loop_heartbeat
 30294-30321  _loop_lag_monitor
 15119-15122  _loop_not_ready
 15012-15080  _loop_watchdog_thread
 20427-20441  _loyalty_add
 20418-20424  _loyalty_get
 20444-20452  _loyalty_top
 16020-16038  _manual_donations_rows
 16041-16043  _manual_donations_total
  8062-8063   _mark_dead
 12510-12539  _marketing_cfg
 12501-12507  _marketing_default_targets
 12496-12498  _marketing_enabled
 12553-12568  _marketing_flavor
 12623-12639  _marketing_loop
 12571-12581  _marketing_post_discord
 12584-12596  _marketing_post_telegram
 12599-12620  _marketing_publish
 12542-12546  _marketing_state_obj
 12549-12550  _marketing_state_save
 29114-29132  _maybe_handle_command
 30631-30655  _maybe_hype_clip
  3764-3787   _migrate_columns
 29389-29400  _mod_is_exempt
 29403-29408  _mod_warn_first
 29411-29414  _mod_warn_text
 17178-17186  _modlog
   889-891    _multistream_targets
  7948-7949   _nc_create_subprocess_exec
  7952-7953   _nc_create_subprocess_shell
 12734-12750  _news_cfg
 12721-12723  _news_enabled
 12788-12829  _news_facts
 12943-12965  _news_generate
 13148-13165  _news_loop
 12726-12731  _news_output_path
 12832-12834  _news_phrase
 12919-12940  _news_phrase_impl
 12763-12770  _news_read
 12753-12756  _news_state_obj
 12759-12760  _news_state_save
 12773-12785  _news_write
 17216-17218  _normalize_ingest
  2231-2248   _note_check_duration
 20573-20581  _oracle_memories
 20839-20873  _oracle_memorize
 20584-20597  _oracle_persona
 20566-20570  _oracle_recent_text
 17515-17523  _ov_atomic_write
 17503-17509  _ov_bar
 19373-19385  _ov_clip_text
 17512-17513  _ov_oneline
 23987-24016  _overlay_push
 17806-17849  _overlay_render_size
 17277-17281  _overlay_session_reset
 23935-23938  _overlay_src_ok
 19536-19546  _own_invites
 16001-16017  _parse_eur
 17801-17803  _parse_size
 25195-25275  _parse_ssh_attacks
  7372-7405   _pause_resume_cmd
  1726-1770   _persist_refreshed_cookies
  1564-1596   _pick_checked_pull_proxy
 10217-10222  _pin_auth_value
 10254-10255  _pin_clear_fail
 10234-10237  _pin_locked
 10240-10251  _pin_note_fail
 10225-10231  _pin_ok
 23825-23827  _piper_available
 23790-23812  _piper_list_voices
 23832-23857  _piper_pick_model
 23869-23916  _piper_say
 23783-23787  _piper_voice_roots
 15536-15571  _post_json_threaded
 17780-17798  _probe_video_size
  1451-1468   _proc_is_recorder
 11675-11686  _proxy_geo_cache_put
 11902-11928  _proxy_pool_refresh_loop
  1530-1561   _proxy_report_recording
 14965-14967  _prune_stall_dumps
 12968-13089  _public_stats
 21101-21127  _push_notify
 10356-10358  _pwa_dir
 11646-11661  _quick_validate_proxy
 15602-15604  _quiet_hours_config
 10321-10354  _rate_guard
 20392-20398  _react_warn
  7856-7895   _reap_proc
  2271-2293   _record_check_outcome
   683-685    _redact_stream_urls
 11829-11899  _refresh_proxy_pool
 23815-23821  _resolve_piper_model
  2065-2155   _resolve_via_html
  2413-2567   _resolve_via_webcast_api_v2
  2630-2692   _resolve_via_ytdlp
 28733-28862  _resolve_youtube_ingest
 22030-22037  _restream_active_platforms
 17262-17273  _restream_active_sources
 21611-21710  _restream_chat_guardian
 17427-17499  _restream_chat_push
 17189-17201  _restream_enabled
 17868-17955  _restream_html_overlay_start
 17958-17971  _restream_html_overlay_stop
  1033-1035   _restream_layout_mode
 17227-17250  _restream_overlay_files
 21995-22027  _restream_platform_state
 22151-22186  _restream_resume_after_restart
 18019-18077  _restream_tts_enqueue_wav
 17742-17774  _restream_tts_feeder
 17739-17740  _restream_tts_fifo_path
 17974-18001  _restream_tts_start
 18003-18017  _restream_tts_stop
 22040-22148  _restream_verify_loop
 27748-27760  _retention_loop
 27707-27745  _retention_scan
  2375-2377   _room_is_abo
  6216-6333   _run_ai_call
 15103-15116  _run_async_from_flask
 24996-24999  _run_priv
 31301-31309  _run_selfcheck_and_exit
 27763-27774  _s3_client
  8065-8111   _safe_send
  4699-4715   _sample_net_throughput
 19427-19435  _save_banned_words_file
  2323-2350   _schedule_next_check
 27666-27704  _scheduler_loop
  3790-3794   _schema_pk
 15124-15129  _scraper_session
 29417-29456  _screen_full
 13680-13717  _sec_headers
  2044-2046   _select_stream_from_data_section
 31114-31298  _selfcheck
  1108-1112   _should_defer_upload
 28174-28209  _shrink_for_discord
 30552-30569  _sign_health_check
 30572-30591  _sign_health_loop
  7965-7976   _spawn
  7979-8009   _spawn_from_flask
 25319-25322  _st_befund
 21336-21577  _start_chat_listener
 15083-15100  _start_loop_watchdog
 13113-13139  _stats_loop
 13092-13095  _stats_output_path
 13098-13110  _stats_write
  8557-8571   _storage_cleanup_loop
 30611-30618  _story_for
  3082-3088   _stream_url_expiry
  3097-3103   _stream_url_is_fresh
  3090-3095   _stream_url_ttl
 19500-19507  _streamer_persona_get
 19482-19488  _streamer_personas_load
 19479-19480  _streamer_personas_path
 19490-19498  _streamer_personas_save
 17694-17698  _studio_chain
 27880-28002  _system_backup
 28005-28033  _system_backup_loop
 11598-11637  _test_proxy
 12384-12393  _testpush_cfg
 12396-12413  _testpush_exec
 12365-12381  _testpush_resolve_live
  8734-8744   _tg_topics_load_into_mem
  8731-8732   _tg_topics_path
  8746-8753   _tg_topics_save
 24529-24577  _tiktok_account_exists
 10200-10208  _token_ok
  8756-8760   _topic_forget
 15622-15633  _tracking_max_duration
  1335-1358   _try_attach_file_handler
 23859-23867  _tts_cleanup
 12269-12272  _tunnel_effective
 23285-23338  _twitch_channel_status
 29459-29601  _twitch_chat_loop
 29275-29376  _twitch_eventsub_loop
 16441-16444  _twitch_oauth_page
  1131-1144   _upload_queue_add
  1155-1157   _upload_queue_count
  1114-1123   _upload_queue_load
  1104-1106   _upload_queue_path
  1146-1153   _upload_queue_remove
  1125-1129   _upload_queue_save
  1159-1197   _upload_window_loop
  7829-7836   _uptime_s
 17204-17213  _url_host
   747-751    _usage_record_claude
  6945-6973   _viewer_sample_loop
  7015-7022   _viewer_stats
 10258-10261  _wants_html
  7839-7853   _warn_empty_env
 30367-30462  _watchdog_loop
 29016-29024  _wchat_thank_ok
 21170-21200  _whisper_get_model
  7926-7933   _whisper_native_section
 20379-20385  _whisper_pool
 21269-21298  _whisper_segments
 21202-21266  _whisper_transcribe
 17525-17687  _write_restream_overlay
 29629-29702  _youtube_api_chat_loop
 23341-23444  _youtube_api_status
 23447-23514  _youtube_channel_status
 29705-29862  _youtube_chat_loop
 28868-28881  _youtube_restream_autoconfig
 28884-28908  _youtube_restream_autoconfig_inner
 28974-29002  _youtube_send
 23619-23660  _youtube_set_channel
 28911-28945  _yt_access_token
 28948-28963  _yt_live_chat_id
 29622-29626  _yt_oauth_configured
 28969-28971  _yt_sendrate_cfg
 29604-29619  _yt_timeout
  2614-2615   _ytdlp_detect_available
  2617-2628   _ytdlp_note_result
 14970-14972  _zombie_child_count
  7706-7730   about
  3965-3969   add_ai_log_entry
  3882-3885   add_archive_entry
  4812-4827   add_archive_rule
  4394-4428   add_recording
  4055-4072   add_tracking
  4489-4506   add_tracking_tag
  6336-6369   ai
  3629-3668   ai_chat
  3702-3712   ai_history_append
  3714-3719   ai_history_clear
  3691-3700   ai_history_load
  3676-3689   ai_rate_limit_check
  6398-6406   aireset
 20710-20729  azrael_chat
 29867-29989  brain_cmd
  3106-3290   build_recording_cmd
  4075-4152   bulk_add_trackings
  7203-7262   bulkadd
  8574-8714   check_all_trackings
  4239-4251   claim_live_transition
 19576-20322  class KickModerator
 18282-19260  class RestreamManager
 12013-12055  classify_proxy_anonymity
  6444-6642   cleanup
  5407-5448   cleanup_old_recordings
  4385-4392   clear_recording
 28619-28684  clip_moment
  4960-5003   cluster_failures
  4643-4692   compute_storage_forecast
  7325-7369   cookies_cmd
  5249-5255   cookies_days_old
  4046-4052   count_trackings_for_chat
  3952-3963   decide_preferred_recorder
  3892-3895   delete_archive_entry
  4829-4837   delete_archive_rule
  5873-6020   diag
 29992-30053  einnahmen_cmd
  4637-4640   find_recordings_by_fingerprint
  3913-3929   finish_recording_attempt
  4184-4194   get_all_active_trackings
  3991-3994   get_all_checks
  4430-4433   get_all_recordings
  4531-4541   get_all_tags_with_counts
  4614-4617   get_annotations_for_recording
  3887-3890   get_archive_entry
  4607-4610   get_bookmarked_recordings
  1793-1910   get_cookie_health
  4480-4486   get_event_log
  3936-3950   get_last_recording_attempt
  2695-2800   get_live_status
  5163-5166   get_manual_recordings
  4622-4625   get_or_compute_inspect_sync
  5483-5527   get_outcome_breakdown
  4588-4596   get_priority_poll_interval
  4790-4799   get_profile_snapshots
  3971-3981   get_recent_ai_log
  3931-3934   get_recent_recording_attempts
  4435-4438   get_recording_by_id
  4600-4603   get_recording_note
  3424-3447   get_redis
  4022-4038   get_stats
  5374-5405   get_storage_stats
  4521-4529   get_tags_for_tracking
  4930-4944   get_tiktok_status_distribution
  4575-4586   get_tracking_priority
  4253-4262   get_tracking_state
  4180-4182   get_trackings_for_group
  5179-5182   get_trash_recordings
  9418-10028  handle_recording_finished
  3812-3837   init_db
  5297-5351   inspect_stream_url
 23982-23984  is_revenue_platform
  4802-4810   list_archive_rules
  5677-5715   live
  8114-8122   live_check_worker
  3499-3533   llm_chat
  3556-3584   llm_chat_sync
  3541-3553   llm_list_models
  4446-4472   log_event
  1385-1418   log_recording_failure
  7519-7568   logs_cmd
 30659-31104  main
  6372-6395   on_ai_media
  7645-7671   on_ai_reply
  7674-7703   on_azrael_mention
  7735-7765   on_callback
 20732-20836  oracle_handle
  7408-7411   pause_tracking
  5537-5542   profile_keyboard
  5258-5294   quick_restart_tracking
  7470-7516   quota
  8491-8554   reaper_loop
  4926-4928   record_tiktok_status
  6411-6441   recstatus
  3449-3457   redis_get_json
  3459-3465   redis_set_json
  4154-4178   remove_tracking
  4508-4519   remove_tracking_tag
 30056-30066  report_cmd
 12058-12060  report_proxy_result
  2158-2185   resolve_tiktok_live_stream
  5174-5177   restore_recording
  7414-7417   resume_tracking
  4840-4920   run_archive_rules
 30069-30274  run_bot
 14892-14939  run_flask
  4718-4763   sample_bandwidth_for_active
  4769-4788   save_profile_snapshot
  3983-3989   save_tiktok_check
  4377-4383   set_recording_file
  4197-4235   set_tracking_paused
  4544-4573   set_tracking_priority
  5169-5172   soft_delete_recording
  8803-9416   split_and_send_video
  5590-5632   start
  3897-3911   start_recording_attempt
  6645-6683   stats
  5144-5161   stop_manual_recording
  7420-7467   stoprec
  6870-6878   summary_cmd
  7571-7642   sysres
  6022-6166   teststream
  5634-5675   tiktok
  7265-7322   topusers
  5752-5809   track
  5717-5749   track_exact
  5823-5871   tracklist
  5010-5142   trigger_manual_recording
  4338-4375   try_acquire_recording_lock
  5185-5244   universal_search
  5811-5821   untrack
  4632-4635   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           class MarketingConfig, class MarketingState, compose, has_content, next_due_ts, should_post, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                build_items, class NewsConfig, class NewsState, item_id, merge, render_json, should_generate
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
trackingdb.py          claim_transition, get_state
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
