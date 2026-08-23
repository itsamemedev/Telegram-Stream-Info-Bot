# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (255)

```
 10574  GET              /                                                dashboard
 15464  GET              /api/abo/status                                  api_abo_status
 10673  GET              /api/active-recordings                           api_active_recordings
 15539  GET              /api/activity-pulse                              api_activity_pulse
 14892  GET              /api/ai-log                                      api_ai_log
 11071  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15299  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23250  GET/POST         /api/audio/config                                api_audio_config
 23280  POST             /api/audio/testtone                              api_audio_testtone
 15405  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15429  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15433  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12349  GET              /api/automation/status                           api_automation_status
 12371  POST             /api/automation/toggle                           api_automation_toggle
 14097  GET              /api/azrael/agents                               api_azrael_agents
 12252  POST             /api/azrael/ask                                  api_azrael_ask
 23486  GET/POST         /api/azrael/context                              api_azrael_context
 13724  GET              /api/azrael/core                                 api_azrael_core
 23620  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23610  GET              /api/azrael/live_status                          api_azrael_live_status
 23628  POST             /api/azrael/live_test                            api_azrael_live_test
 14106  GET              /api/azrael/memories                             api_azrael_memories
 23676  POST             /api/azrael/persona                              api_azrael_persona_set
 23667  GET              /api/azrael/personas                             api_azrael_personas
 23704  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23459  POST             /api/azrael/react                                api_azrael_react
 23495  GET              /api/azrael/reaction                             api_azrael_reaction
 23647  GET              /api/azrael/reactions                            api_azrael_reactions
 23697  GET              /api/azrael/transcript                           api_azrael_transcript
 23582  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23557  GET              /api/azrael/voices                               api_azrael_voices
 23721  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11166  GET              /api/backoff-watch                               api_backoff_watch
 14663  POST             /api/backup/run                                  api_backup_run
 14629  GET              /api/backup/status                               api_backup_status
 14618  POST             /api/backup/system                               api_backup_system
 15371  GET              /api/bandwidth/live                              api_bandwidth_live
 15284  GET              /api/bookmarks                                   api_bookmarks_list
 11429  GET              /api/brain                                       api_brain
 11366  GET              /api/brain/alarms                                api_brain_alarms
 11351  GET              /api/brain/creator                               api_brain_creator
 11328  GET              /api/brain/graph                                 api_brain_graph
 11389  GET              /api/brain/growth                                api_brain_growth
 10170  GET              /api/brain/health                                api_brain_health
 24202  GET              /api/channel/categories                          api_channel_categories
 24208  POST             /api/channel/set                                 api_channel_set
 24018  GET              /api/channels/status                             api_channels_status
 22851  POST             /api/chat/send                                   api_chat_send
 14364  GET              /api/chat/send_status                            api_chat_send_status
 10654  GET              /api/checks                                      api_checks
 23523  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23506  GET              /api/clips                                       api_clips
 23539  POST/DELETE      /api/clips/clear                                 api_clips_clear
 23125  GET              /api/cohost                                      api_cohost
 23137  POST             /api/cohost/config                               api_cohost_config
 16103  GET              /api/community/stats                             api_community_stats
 25202  POST             /api/config/restore                              api_config_restore
 25187  GET              /api/config/snapshot                             api_config_snapshot
 15562  GET              /api/cookies/age                                 api_cookies_age
 10721  GET              /api/cookies/health                              api_cookies_health
 10728  POST             /api/cookies/update                              api_cookies_update
 25153  GET              /api/data/export                                 api_data_export
 16618  GET              /api/db/export                                   api_db_export
 16645  POST             /api/db/import                                   api_db_import
 16605  GET              /api/db/summary                                  api_db_summary
 23051  GET              /api/debug/threads                               api_debug_threads
 26088  GET              /api/defense/attacks                             api_defense_attacks
 26055  GET              /api/defense/crowdsec                            api_defense_crowdsec
 26073  GET              /api/defense/fail2ban                            api_defense_fail2ban
 25779  GET              /api/defense/overview                            api_defense_overview
 14725  POST             /api/discord/announce                            api_discord_announce
 14453  GET              /api/discord/clips_week                          api_discord_clips_week
 14669  GET              /api/discord/community                           api_discord_community
 14392  GET              /api/discord/invite                              api_discord_invite
 13855  GET              /api/discord/overview                            api_discord_overview
 13941  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16180  POST             /api/donations/add                               api_donations_add
 16213  GET              /api/donations/manual                            api_donations_manual
 16221  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16116  POST             /api/donations/reset                             api_donations_reset
 16237  GET              /api/donations/summary                           api_donations_summary
 15353  GET              /api/events                                      api_events
 14500  GET              /api/events/stream                               api_events_stream
 17273  GET              /api/evolution/changelog                         api_evolution_changelog
 17258  GET              /api/evolution/history                           api_evolution_history
 17198  GET              /api/evolution/learned                           api_evolution_learned
 17220  GET              /api/evolution/proposals                         api_evolution_proposals
 17241  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17188  POST             /api/evolution/run                               api_evolution_run
 17288  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17153  GET              /api/evolution/status                            api_evolution_status
 16452  GET              /api/finanzamt/entries                           api_finanzamt_entries
 16472  POST             /api/finanzamt/entry                             api_finanzamt_add
 16499  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15366  GET              /api/forecast/storage                            api_forecast_storage
 12387  GET              /api/freeai/status                               api_freeai_status
 13797  GET              /api/health                                      api_health
 15384  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15380  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23174  GET              /api/highlights                                  api_highlights
 23186  POST             /api/highlights/config                           api_highlights_config
 24059  GET              /api/kick/channel                                api_kick_channel
 24080  POST             /api/kick/channel                                api_kick_channel_set
 13524  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13592  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13570  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13509  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13549  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23298  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23367  POST             /api/kickmod/config                              api_kickmod_config
 23412  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23426  GET              /api/kickmod/learned                             api_kickmod_learned
 23453  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23433  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 23764  POST             /api/kickmod/say                                 api_kickmod_say
 23740  POST             /api/kickmod/start                               api_kickmod_start
 23338  GET              /api/kickmod/status                              api_kickmod_status
 23751  POST             /api/kickmod/stop                                api_kickmod_stop
 10506  POST             /api/login                                       dashboard_login_submit
 16088  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12802  POST             /api/marketing/config                            api_marketing_config
 12827  GET              /api/marketing/preview                           api_marketing_preview
 12837  POST             /api/marketing/send-now                          api_marketing_send_now
 12776  GET              /api/marketing/status                            api_marketing_status
 12794  POST             /api/marketing/toggle                            api_marketing_toggle
 23201  GET              /api/moderation/feed                             api_moderation_feed
 13355  POST             /api/news/config                                 api_news_config
 13321  GET              /api/news/creators                               api_news_creators
 13332  POST             /api/news/creators/generate                      api_news_creators_generate
 13397  POST             /api/news/generate-now                           api_news_generate_now
 13392  GET              /api/news/items                                  api_news_items
 13383  GET              /api/news/preview                                api_news_preview
 13302  GET              /api/news/status                                 api_news_status
 13347  POST             /api/news/toggle                                 api_news_toggle
 15945  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14329  GET              /api/notify/status                               api_notify_status
 14340  POST             /api/notify/test                                 api_notify_test
 14315  GET              /api/ops/audit                                   api_ops_audit
 16016  GET              /api/ops/db-stats                                api_ops_db_stats
 16044  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14121  GET              /api/ops/errors                                  api_ops_errors
 15965  GET              /api/ops/healthcheck                             api_ops_healthcheck
 16700  GET              /api/ops/log-tail                                api_ops_log_tail
 12232  GET              /api/ops/logtail                                 api_ops_logtail
 14062  GET              /api/ops/metrics                                 api_ops_metrics
 14045  GET              /api/ops/resource_history                        api_ops_resource_history
 16674  GET              /api/ops/version                                 api_ops_version
 10924  GET              /api/outcomes                                    api_outcomes
 24683  POST             /api/overlay/config                              api_overlay_config
 24670  POST             /api/overlay/event                               api_overlay_event
 24575  GET              /api/overlay/state                               api_overlay_state
 10957  GET              /api/profile/<username>                          api_profile
 15570  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15392  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15518  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15495  GET              /api/proxy/trend                                 api_proxy_trend
 13276  GET              /api/public/stats                                api_public_stats
 10608  GET              /api/pulse                                       api_pulse
 14916  GET              /api/recording-attempts                          api_recording_attempts
 22786  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 22764  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 22805  POST             /api/restream/<int:rid>/start                    api_restream_start
 23072  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24537  GET              /api/restream/chatfeed                           api_restream_chatfeed
 22740  POST             /api/restream/create                             api_restream_create
 13600  GET              /api/restream/deck                               api_restream_deck
 12323  GET              /api/restream/health                             api_restream_health
 24559  POST             /api/restream/layout                             api_restream_layout
 22713  GET              /api/restream/list                               api_restream_list
 12296  POST             /api/restream/report                             api_restream_report
 23085  POST             /api/restream/start_all                          api_restream_start_all
 23111  POST             /api/restream/stop_all                           api_restream_stop_all
 12550  GET              /api/restream/testpush                           api_testpush_status
 12575  POST             /api/restream/testpush                           api_testpush_run
 16353  GET              /api/restream/verify                             api_restream_verify
 14431  GET              /api/retention/preview                           api_retention_preview
 14440  POST             /api/retention/run                               api_retention_run
 25268  POST             /api/schedule/add                                api_schedule_add
 25258  GET              /api/schedule/list                               api_schedule_list
 25293  POST             /api/schedule/remove                             api_schedule_remove
 15269  GET              /api/search                                      api_search
 25826  GET              /api/selftest                                    api_selftest
 22822  GET              /api/shield/stats                                api_shield_stats
 10627  GET              /api/stats                                       api_stats
 15533  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15460  GET              /api/stats/tiktok-status                         api_tiktok_status
 25233  GET              /api/stats/timeline                              api_stats_timeline
 10695  GET              /api/storage                                     api_storage
 10702  POST             /api/storage/cleanup                             api_storage_cleanup
 15446  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12273  GET              /api/stream/timeline                             api_stream_timeline
 13929  GET              /api/stream/transcript                           api_stream_transcript
 24901  GET              /api/streamer/compare                            api_streamer_compare
 25100  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14405  GET              /api/streamer/detail                             api_streamer_detail
 25125  GET              /api/streamer/digest/<username>                  api_streamer_digest
 25005  GET              /api/streamer/dormant                            api_streamer_dormant
 25081  GET              /api/streamer/exists/<username>                  api_streamer_exists
 24960  GET              /api/streamer/journal/<username>                 api_streamer_journal
 24925  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 24985  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13764  GET              /api/streamers/wall                              api_streamers_wall
 10844  GET              /api/summary/preview                             api_summary_preview
 14981  GET              /api/system                                      api_system
 16301  GET              /api/system/check_timing                         api_check_timing
 16586  GET              /api/system/config_drift                         api_config_drift
 13965  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14176  GET              /api/system/preflight                            api_system_preflight
 14302  GET              /api/system/preflight_history                    api_system_preflight_history
 14565  GET              /api/system/resilience                           api_system_resilience
 15304  GET              /api/tags                                        api_tags_list
 10668  GET              /api/top                                         api_top
 12206  GET              /api/trackings                                   api_trackings
 15834  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 15867  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15340  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15553  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 15896  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15326  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 14755  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 14802  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 14831  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 14813  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10861  POST             /api/trackings/bulk                              api_trackings_bulk
 14770  GET              /api/trackings/export                            api_trackings_export
 15308  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15608  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11221  GET              /api/trend-7d                                    api_trend_7d
 23571  GET              /api/tts/<fn>                                    api_tts_file
 12430  POST             /api/tunnel/set                                  api_tunnel_set
 12409  GET              /api/tunnel/status                               api_tunnel_status
 12441  POST             /api/tunnel/test                                 api_tunnel_test
 12422  POST             /api/tunnel/toggle                               api_tunnel_toggle
 16558  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16535  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16517  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 24711  GET              /api/upload_window                               api_upload_window
 10938  GET              /api/userstats                                   api_userstats
 13408  GET              /api/version                                     api_version
 16414  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16435  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16399  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16383  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 29506  GET              /api/youtube/sendrate                            api_youtube_sendrate
 14954  GET              /archive/<int:eid>/download                      archive_download
 15011  GET              /download/<int:recording_id>                     download
 14877  GET              /health                                          health
 23020  GET              /healthz                                         healthz
 10495  GET              /login                                           dashboard_login_page
 10529  GET              /logout                                          dashboard_logout
 10536  GET              /manifest.webmanifest                            pwa_manifest
 13993  GET              /metrics                                         api_prometheus_metrics
 24520  GET              /overlay                                         overlay_page
 10560  GET              /pwa-icon-<variant>.png                          pwa_icon
 10546  GET              /sw.js                                           pwa_service_worker
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
 26531  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 26990  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 26622  /assign_role            Rolle/Gruppe einem Mitglied geben
 26668  /ban                    Mitglied bannen
 27322  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 27246  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27286  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 27271  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 27113  /clips                  Letzte Highlight-Clips eines Users
 26583  /create_category        Kategorie anlegen
 26552  /create_channel         Text-Channel anlegen (optional in Kategorie)
 26611  /create_group           Nutzergruppe (= Rolle) anlegen
 26594  /create_role            Rolle / Nutzergruppe anlegen
 26568  /create_voice           Voice-Channel anlegen
 26904  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 27020  /event                  Community-Event ankündigen (Admin) — mit Countdown
 27063  /events                 Kommende Community-Events anzeigen
 27159  /follow                 Bei Live-Gang eines Streamers gepingt werden
 27143  /help                   Alle Bot-Befehle anzeigen
 26657  /kick                   Mitglied kicken
 26886  /leaderboard            Top-10 der Community nach XP
 27099  /livenow                Welche getrackten User sind gerade live
 27129  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 26960  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 26692  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 26872  /rank                   Dein Level und Rang anzeigen
 27086  /recstatus              Aktuell laufende Aufnahmen
 26633  /remove_role            Rolle/Gruppe entfernen
 26545  /restream_status        Restream-Status
 26644  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 26837  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 26855  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 27185  /stats                  Statistik zu einem getrackten Streamer
 26457  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 27481  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 27378  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 27354  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 26679  /timeout                Mitglied stummschalten (Minuten)
 27257  /topstreamers           Rangliste der Streamer nach Aufnahmen
 26487  /track                  TikTok-User tracken
 26471  /tracklist              Getrackte TikTok-User dieses Servers
 27174  /unfollow               Live-Pings für einen Streamer abbestellen
 26520  /untrack                TikTok-User nicht mehr tracken
 27207  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 27231  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 27965  on_member_join
 27927  on_message
 27568  on_raw_reaction_add
 28000  on_ready
```

## Top-Level-Symbole in bot_v37.py (552 Funktionen, 2 Klassen)

```
  2426-2427   _abo_key
  2447-2465   _abo_probe_dump
 25368-25378  _active_recorder_sync
 20010-20017  _ad_allowlist
 21132-21138  _agent_for
 25380-25398  _ai_calls_total_sync
 21141-21157  _ai_telemetry
 21639-21657  _alert
 28113-28163  _alert_monitor_loop
 28537-28599  _announce_loop
  3368-3371   _anthropic_key
  3378-3380   _anthropic_model
 10298-10301  _arg_int
  2418-2423   _as_dict
 17870-17875  _audio_cfg
 21793-21815  _audio_tap_cmd
 10431-10442  _auth_cookie
 10398-10427  _auth_guard
  1574-1579   _auto_on
 22689-22707  _auto_restream_loop
 29667-29682  _azrael_broadcast_reply
 29567-29589  _azrael_chat_reply
 29550-29564  _azrael_chat_should_reply
 13002-13020  _azrael_creator_take
 29595-29597  _azrael_gate_cfg
 21162-21176  _azrael_live_state
 24419-24433  _azrael_overlay_state
 21522-21576  _azrael_proactive_loop
 20981-21037  _azrael_reaction_to_chats
 29600-29607  _azrael_reply_all_chats
 29537-29547  _azrael_self_names
 29635-29664  _azrael_send_to
 21179-21200  _azrael_system
 28277-28280  _backup_active
 28358-28371  _backup_loop
 19898-19899  _badwords_path
 28078-28087  _brain_growth_loop
 11297-11324  _brain_growth_snapshot
  2354-2374   _brain_hint_delay
 11289-11291  _brain_history_for
  6790-6818   _brain_notify
 11266-11287  _brain_record
 11293-11295  _brain_stream_recent
 14479-14496  _browser_push
  6834-6921   _build_daily_summary
  2857-3037   _build_native_cmd
 18218-18405  _build_restream_cmd
  3081-3114   _build_ytdlp_cmd
 25320-25327  _cached_probe
  5612-5639   _can_stop_tracking
  1754-1776   _capture_set_cookies
 15656-15659  _cfg_get
 15662-15664  _cfg_set
 24163-24198  _channel_set_all
 17468-17471  _chat_connected
 17474-17490  _chat_disconnected
  8863-8874   _chat_is_forum
 17510-17512  _chat_sanitize
 17514-17523  _chat_src_ok
 17453-17465  _chat_stat
 17493-17496  _chat_stats_snapshot
  3643-3654   _check_ai_alive_sync
  3657-3669   _check_ai_models_sync
 25329-25342  _check_redis_alive_sync
 25344-25364  _check_redis_version_sync
 11896-11939  _classify_pool_anonymity
 11942-11959  _classify_pool_anonymity_bg
   754-758    _claude_chat_sync_metered
 10323-10330  _client_ip
 28631-28658  _clip_prune
 28661-28671  _clip_recfile_for
 29187-29193  _clip_should_velocity
 28712-28794  _clip_to_discord
  3541-3550   _close_ai_session
 29711-29726  _cohost_broadcast
 29693-29697  _cohost_cfg
 29752-29764  _cohost_fire_highlight
 29700-29708  _cohost_gate
 29729-29749  _cohost_highlight
 28843-28877  _community_events_loop
 11120-11122  _conv_messages
  7214-7254   _cookie_alarm_loop
  1826-1830   _cookie_autorefresh_info
  1731-1735   _cookie_header
 14529-14561  _cpu_load_snapshot
  3851-3863   _create_index_safe
 12970-12985  _creator_activity
 13026-13049  _creator_dossier_generate
 12988-12999  _creator_facts_line
 25581-25687  _crowdsec_status
 25547-25578  _crowdsec_via_lapi
 25412-25430  _cscli_bin
 25436-25449  _cscli_path
  7107-7132   _daily_summary_loop
 25467-25484  _darf_journal_lesen
 28090-28110  _db_maintenance_loop
  7079-7104   _db_vacuum_loop
 20033-20057  _detect_foreign_ad
  1331-1342   _diag_path_owner
 21428-21472  _director_finalize
 22239-22246  _director_for
 21377-21425  _director_mark
 29081-29116  _disc_automod_check
 29054-29060  _disc_state_get
 29063-29070  _disc_state_set
 26130-26143  _discord_guild_filesize_bytes
 26329-26338  _discord_invite
 29015-29051  _discord_live_thread
 21579-21591  _discord_notify
 26230-26255  _discord_ops_alert
 28913-29011  _discord_post_user
 26394-28075  _discord_run_once
 26268-26326  _discord_start
 28602-28608  _discord_stop
 26151-26153  _discord_upload_limit_label
 26146-26148  _discord_upload_limit_mb
  7135-7209   _disk_alarm_loop
 30983-31032  _disk_autoclean
 31035-31048  _disk_guard_loop
 30975-30980  _disk_pct
 24476-24479  _donations_unknown_count
 17827-17829  _drawtext_chain
 15108-15110  _dump_all_threads
 11821-11885  _enrich_proxies_with_geo
  1971-2015   _ensure_cookie_file_netscape
 26341-26391  _ensure_discord_invite
 28808-28840  _ensure_error_channel
 12064-12101  _ensure_proxy_ready
  8876-8899   _ensure_topic
   637-639    _env_int
   642-644    _env_int_range
 28880-28910  _error_channel_loop
 21623-21636  _event_webhook
 16761-16767  _evo_build_dir
 16770-16777  _evo_version
 17053-17134  _evolution_cycle
 16786-16806  _evolution_llm_note
 17137-17147  _evolution_loop
 16809-17050  _evolution_write_build
  6232-6266   _extract_file_payload
  2103-2105   _extract_urls_from_streamurl_node
 25452-25459  _f2b_sudo_hint
 21659-21661  _faster_whisper_available
 19922-19934  _fetch_ldnoobw_de
 11710-11728  _fetch_proxy_list
 22073-22101  _fetch_tiktok_room_id
   688-691    _ff_cmd
 15779-15792  _ffmpeg_version_str
 17990-17995  _find_chromium
  3074-3078   _find_external_recorder
  2108-2110   _find_stream_urls
 15707-15732  _fire_webhooks
  7990-7999   _fork_safe
   769-778    _freeai_chat_sync_metered
 25502-25544  _geo_lookup_ips
  3530-3539   _get_ai_session
  7824-7864   _get_live_info
  2644-2651   _get_resolve_semaphore
  8225-8590   _handle_single_tracking
 30827-30829  _hb
 30832-30849  _hb_while
 17528-17530  _highlight_cfg
 17533-17562  _highlight_observe
 17998-18003  _htmlov_screenshot_cmd
 21817-21827  _httpx_proxy
 15740-15752  _in_quiet_hours
 31816-31847  _install_fast_eventloop
 10193-10247  _install_fast_json
 15113-15129  _install_faulthandler
 22932-22941  _intel_ensure_schema
 22979-23010  _intel_index_loop
 22953-22963  _intel_index_one
 22944-22950  _intel_semantic
  5601-5610   _is_authorized
  8155-8161   _is_dead
  2093-2095   _is_hevc
 25487-25493  _is_private_ip
  1477-1484   _is_process_running
  6820-6831   _is_quiet_hours
  1139-1148   _is_upload_window
 10282-10295  _json_error_handler
  7037-7067   _kick_broadcaster_id
 12476-12495  _kick_channel_live
  6954-6996   _kick_follower_count
 13487-13500  _kick_oauth_exchange
 13503-13505  _kick_oauth_page
 13446-13450  _kick_redirect_public
 13437-13443  _kick_redirect_source
 13423-13434  _kick_redirect_uri
  6939-6941   _kick_slug
 13453-13484  _kick_user_token
  3900-3903   _kind_from_filename
 15769-15774  _latest_popularity
 19944-19950  _learned_load
 19941-19942  _learned_path
 19952-19960  _learned_save
 22454-22484  _live_react_loop
 22250-22443  _live_react_worker
 21040-21051  _live_transcript_push
 22445-22452  _live_users
 21475-21519  _living_title_loop
 19901-19909  _load_banned_words_file
  1652-1725   _load_cookies_dict
 28283-28355  _local_backup_scan
 10264-10278  _log_5xx
 18413-18425  _looks_like_codec_err
 18408-18410  _looks_like_source_expired
  8071-8101   _loop_fehler
 15133-15142  _loop_heartbeat
 30797-30824  _loop_lag_monitor
 15252-15255  _loop_not_ready
 15145-15213  _loop_watchdog_thread
 20920-20934  _loyalty_add
 20911-20917  _loyalty_get
 20937-20945  _loyalty_top
 16153-16171  _manual_donations_rows
 16174-16176  _manual_donations_total
  8163-8164   _mark_dead
 12643-12672  _marketing_cfg
 12634-12640  _marketing_default_targets
 12629-12631  _marketing_enabled
 12686-12701  _marketing_flavor
 12756-12772  _marketing_loop
 12704-12714  _marketing_post_discord
 12717-12729  _marketing_post_telegram
 12732-12753  _marketing_publish
 12675-12679  _marketing_state_obj
 12682-12683  _marketing_state_save
 29614-29632  _maybe_handle_command
 31134-31158  _maybe_hype_clip
  3818-3841   _migrate_columns
 29891-29902  _mod_is_exempt
 29905-29910  _mod_warn_first
 29913-29916  _mod_warn_text
 17316-17324  _modlog
   892-894    _multistream_targets
  8002-8003   _nc_create_subprocess_exec
  8006-8007   _nc_create_subprocess_shell
 12867-12883  _news_cfg
 12854-12856  _news_enabled
 12921-12962  _news_facts
 13076-13098  _news_generate
 13281-13298  _news_loop
 12859-12864  _news_output_path
 12965-12967  _news_phrase
 13052-13073  _news_phrase_impl
 12896-12903  _news_read
 12886-12889  _news_state_obj
 12892-12893  _news_state_save
 12906-12918  _news_write
 17354-17356  _normalize_ingest
  2285-2302   _note_check_duration
 21066-21074  _oracle_memories
 21332-21366  _oracle_memorize
 21077-21090  _oracle_persona
 21059-21063  _oracle_recent_text
 17653-17661  _ov_atomic_write
 17641-17647  _ov_bar
 19857-19869  _ov_clip_text
 17650-17651  _ov_oneline
 24487-24516  _overlay_push
 17944-17987  _overlay_render_size
 17415-17419  _overlay_session_reset
 24435-24438  _overlay_src_ok
 20020-20030  _own_invites
 16134-16150  _parse_eur
 17939-17941  _parse_size
 25695-25775  _parse_ssh_attacks
  7426-7459   _pause_resume_cmd
  1780-1824   _persist_refreshed_cookies
  1618-1650   _pick_checked_pull_proxy
 10350-10355  _pin_auth_value
 10387-10388  _pin_clear_fail
 10367-10370  _pin_locked
 10373-10384  _pin_note_fail
 10358-10364  _pin_ok
 24325-24327  _piper_available
 24290-24312  _piper_list_voices
 24332-24357  _piper_pick_model
 24369-24416  _piper_say
 24283-24287  _piper_voice_roots
 15669-15704  _post_json_threaded
 17918-17936  _probe_video_size
  1505-1522   _proc_is_recorder
 11808-11819  _proxy_geo_cache_put
 12035-12061  _proxy_pool_refresh_loop
  1584-1615   _proxy_report_recording
 15098-15100  _prune_stall_dumps
 13101-13222  _public_stats
 21594-21620  _push_notify
 10489-10491  _pwa_dir
 11779-11794  _quick_validate_proxy
 15735-15737  _quiet_hours_config
 10454-10487  _rate_guard
 20885-20891  _react_warn
  7910-7949   _reap_proc
  2325-2347   _record_check_outcome
   683-685    _redact_stream_urls
 11962-12032  _refresh_proxy_pool
 24315-24321  _resolve_piper_model
  2119-2209   _resolve_via_html
  2467-2621   _resolve_via_webcast_api_v2
  2684-2746   _resolve_via_ytdlp
 29233-29362  _resolve_youtube_ingest
 22523-22530  _restream_active_platforms
 17400-17411  _restream_active_sources
 22104-22203  _restream_chat_guardian
 17565-17637  _restream_chat_push
 17327-17339  _restream_enabled
 18006-18093  _restream_html_overlay_start
 18096-18109  _restream_html_overlay_stop
  1087-1089   _restream_layout_mode
 17365-17388  _restream_overlay_files
 22488-22520  _restream_platform_state
 22651-22686  _restream_resume_after_restart
 18157-18215  _restream_tts_enqueue_wav
 17880-17912  _restream_tts_feeder
 17877-17878  _restream_tts_fifo_path
 18112-18139  _restream_tts_start
 18141-18155  _restream_tts_stop
 22533-22648  _restream_verify_loop
 28248-28260  _retention_loop
 28207-28245  _retention_scan
  2429-2431   _room_is_abo
  6270-6387   _run_ai_call
 15236-15249  _run_async_from_flask
 25496-25499  _run_priv
 31804-31812  _run_selfcheck_and_exit
 28263-28274  _s3_client
  8166-8212   _safe_send
  4753-4769   _sample_net_throughput
 19911-19919  _save_banned_words_file
  2377-2404   _schedule_next_check
 28166-28204  _scheduler_loop
  3844-3848   _schema_pk
 15257-15262  _scraper_session
 29919-29958  _screen_full
 13813-13850  _sec_headers
  2098-2100   _select_stream_from_data_section
 31617-31801  _selfcheck
  1162-1166   _should_defer_upload
 28674-28709  _shrink_for_discord
 31055-31072  _sign_health_check
 31075-31094  _sign_health_loop
  8019-8030   _spawn
  8033-8063   _spawn_from_flask
 25819-25822  _st_befund
 21829-22070  _start_chat_listener
 15216-15233  _start_loop_watchdog
 13246-13272  _stats_loop
 13225-13228  _stats_output_path
 13231-13243  _stats_write
  8658-8672   _storage_cleanup_loop
 31114-31121  _story_for
  3136-3142   _stream_url_expiry
  3151-3157   _stream_url_is_fresh
  3144-3149   _stream_url_ttl
 19984-19991  _streamer_persona_get
 19966-19972  _streamer_personas_load
 19963-19964  _streamer_personas_path
 19974-19982  _streamer_personas_save
 17832-17836  _studio_chain
 28380-28502  _system_backup
 28505-28533  _system_backup_loop
 11731-11770  _test_proxy
 12517-12526  _testpush_cfg
 12529-12546  _testpush_exec
 12498-12514  _testpush_resolve_live
  8835-8845   _tg_topics_load_into_mem
  8832-8833   _tg_topics_path
  8847-8854   _tg_topics_save
 25029-25077  _tiktok_account_exists
 10333-10341  _token_ok
  8857-8861   _topic_forget
 15755-15766  _tracking_max_duration
  1389-1412   _try_attach_file_handler
 24359-24367  _tts_cleanup
 12402-12405  _tunnel_effective
 23785-23838  _twitch_channel_status
 29961-30104  _twitch_chat_loop
 29775-29878  _twitch_eventsub_loop
 16579-16582  _twitch_oauth_page
  1185-1198   _upload_queue_add
  1209-1211   _upload_queue_count
  1168-1177   _upload_queue_load
  1158-1160   _upload_queue_path
  1200-1207   _upload_queue_remove
  1179-1183   _upload_queue_save
  1213-1251   _upload_window_loop
  7883-7890   _uptime_s
 17342-17351  _url_host
   747-751    _usage_record_claude
  8104-8148   _verbindung_verloren
  6999-7027   _viewer_sample_loop
  7069-7076   _viewer_stats
 10391-10394  _wants_html
  7893-7907   _warn_empty_env
 30870-30965  _watchdog_loop
 29516-29524  _wchat_thank_ok
 21663-21693  _whisper_get_model
  7980-7987   _whisper_native_section
 20872-20878  _whisper_pool
 21762-21791  _whisper_segments
 21695-21759  _whisper_transcribe
 17663-17825  _write_restream_overlay
 30132-30205  _youtube_api_chat_loop
 23841-23944  _youtube_api_status
 23947-24014  _youtube_channel_status
 30208-30365  _youtube_chat_loop
 29368-29381  _youtube_restream_autoconfig
 29384-29408  _youtube_restream_autoconfig_inner
 29474-29502  _youtube_send
 24119-24160  _youtube_set_channel
 29411-29445  _yt_access_token
 29448-29463  _yt_live_chat_id
 30125-30129  _yt_oauth_configured
 29469-29471  _yt_sendrate_cfg
 30107-30122  _yt_timeout
  2668-2669   _ytdlp_detect_available
  2671-2682   _ytdlp_note_result
 15103-15105  _zombie_child_count
  7760-7784   about
  4019-4023   add_ai_log_entry
  3936-3939   add_archive_entry
  4866-4881   add_archive_rule
  4448-4482   add_recording
  4109-4126   add_tracking
  4543-4560   add_tracking_tag
  6390-6423   ai
  3683-3722   ai_chat
  3756-3766   ai_history_append
  3768-3773   ai_history_clear
  3745-3754   ai_history_load
  3730-3743   ai_rate_limit_check
  6452-6460   aireset
 21203-21222  azrael_chat
 30370-30492  brain_cmd
  3160-3344   build_recording_cmd
  4129-4206   bulk_add_trackings
  7257-7316   bulkadd
  8675-8815   check_all_trackings
  4293-4305   claim_live_transition
 20060-20815  class KickModerator
 18428-19744  class RestreamManager
 12146-12188  classify_proxy_anonymity
  6498-6696   cleanup
  5461-5502   cleanup_old_recordings
  4439-4446   clear_recording
 29119-29184  clip_moment
  5014-5057   cluster_failures
  4697-4746   compute_storage_forecast
  7379-7423   cookies_cmd
  5303-5309   cookies_days_old
  4100-4106   count_trackings_for_chat
  4006-4017   decide_preferred_recorder
  3946-3949   delete_archive_entry
  4883-4891   delete_archive_rule
  5927-6074   diag
 30495-30556  einnahmen_cmd
  4691-4694   find_recordings_by_fingerprint
  3967-3983   finish_recording_attempt
  4238-4248   get_all_active_trackings
  4045-4048   get_all_checks
  4484-4487   get_all_recordings
  4585-4595   get_all_tags_with_counts
  4668-4671   get_annotations_for_recording
  3941-3944   get_archive_entry
  4661-4664   get_bookmarked_recordings
  1847-1964   get_cookie_health
  4534-4540   get_event_log
  3990-4004   get_last_recording_attempt
  2749-2854   get_live_status
  5217-5220   get_manual_recordings
  4676-4679   get_or_compute_inspect_sync
  5537-5581   get_outcome_breakdown
  4642-4650   get_priority_poll_interval
  4844-4853   get_profile_snapshots
  4025-4035   get_recent_ai_log
  3985-3988   get_recent_recording_attempts
  4489-4492   get_recording_by_id
  4654-4657   get_recording_note
  3478-3501   get_redis
  4076-4092   get_stats
  5428-5459   get_storage_stats
  4575-4583   get_tags_for_tracking
  4984-4998   get_tiktok_status_distribution
  4629-4640   get_tracking_priority
  4307-4316   get_tracking_state
  4234-4236   get_trackings_for_group
  5233-5236   get_trash_recordings
  9519-10161  handle_recording_finished
  3866-3891   init_db
  5351-5405   inspect_stream_url
 24482-24484  is_revenue_platform
  4856-4864   list_archive_rules
  5731-5769   live
  8215-8223   live_check_worker
  3553-3587   llm_chat
  3610-3638   llm_chat_sync
  3595-3607   llm_list_models
  4500-4526   log_event
  1439-1472   log_recording_failure
  7573-7622   logs_cmd
 31162-31607  main
  6426-6449   on_ai_media
  7699-7725   on_ai_reply
  7728-7757   on_azrael_mention
  7789-7819   on_callback
 21225-21329  oracle_handle
  7462-7465   pause_tracking
  5591-5596   profile_keyboard
  5312-5348   quick_restart_tracking
  7524-7570   quota
  8592-8655   reaper_loop
  4980-4982   record_tiktok_status
  6465-6495   recstatus
  3503-3511   redis_get_json
  3513-3519   redis_set_json
  4208-4232   remove_tracking
  4562-4573   remove_tracking_tag
 30559-30569  report_cmd
 12191-12193  report_proxy_result
  2212-2239   resolve_tiktok_live_stream
  5228-5231   restore_recording
  7468-7471   resume_tracking
  4894-4974   run_archive_rules
 30572-30777  run_bot
 15025-15072  run_flask
  4772-4817   sample_bandwidth_for_active
  4823-4842   save_profile_snapshot
  4037-4043   save_tiktok_check
  4431-4437   set_recording_file
  4251-4289   set_tracking_paused
  4598-4627   set_tracking_priority
  5223-5226   soft_delete_recording
  8904-9517   split_and_send_video
  5644-5686   start
  3951-3965   start_recording_attempt
  6699-6737   stats
  5198-5215   stop_manual_recording
  7474-7521   stoprec
  6924-6932   summary_cmd
  7625-7696   sysres
  6076-6220   teststream
  5688-5729   tiktok
  7319-7376   topusers
  5806-5863   track
  5771-5803   track_exact
  5877-5925   tracklist
  5064-5196   trigger_manual_recording
  4392-4429   try_acquire_recording_lock
  5239-5298   universal_search
  5865-5875   untrack
  4686-4689   update_recording_fingerprint
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
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
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
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
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
