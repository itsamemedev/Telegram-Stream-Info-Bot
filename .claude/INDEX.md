# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (255)

```
 10479  GET              /                                                dashboard
 15369  GET              /api/abo/status                                  api_abo_status
 10578  GET              /api/active-recordings                           api_active_recordings
 15444  GET              /api/activity-pulse                              api_activity_pulse
 14797  GET              /api/ai-log                                      api_ai_log
 10976  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15204  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23101  GET/POST         /api/audio/config                                api_audio_config
 23131  POST             /api/audio/testtone                              api_audio_testtone
 15310  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15334  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15338  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12254  GET              /api/automation/status                           api_automation_status
 12276  POST             /api/automation/toggle                           api_automation_toggle
 14002  GET              /api/azrael/agents                               api_azrael_agents
 12157  POST             /api/azrael/ask                                  api_azrael_ask
 23337  GET/POST         /api/azrael/context                              api_azrael_context
 13629  GET              /api/azrael/core                                 api_azrael_core
 23471  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23461  GET              /api/azrael/live_status                          api_azrael_live_status
 23479  POST             /api/azrael/live_test                            api_azrael_live_test
 14011  GET              /api/azrael/memories                             api_azrael_memories
 23527  POST             /api/azrael/persona                              api_azrael_persona_set
 23518  GET              /api/azrael/personas                             api_azrael_personas
 23555  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23310  POST             /api/azrael/react                                api_azrael_react
 23346  GET              /api/azrael/reaction                             api_azrael_reaction
 23498  GET              /api/azrael/reactions                            api_azrael_reactions
 23548  GET              /api/azrael/transcript                           api_azrael_transcript
 23433  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23408  GET              /api/azrael/voices                               api_azrael_voices
 23572  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11071  GET              /api/backoff-watch                               api_backoff_watch
 14568  POST             /api/backup/run                                  api_backup_run
 14534  GET              /api/backup/status                               api_backup_status
 14523  POST             /api/backup/system                               api_backup_system
 15276  GET              /api/bandwidth/live                              api_bandwidth_live
 15189  GET              /api/bookmarks                                   api_bookmarks_list
 11334  GET              /api/brain                                       api_brain
 11271  GET              /api/brain/alarms                                api_brain_alarms
 11256  GET              /api/brain/creator                               api_brain_creator
 11233  GET              /api/brain/graph                                 api_brain_graph
 11294  GET              /api/brain/growth                                api_brain_growth
 10075  GET              /api/brain/health                                api_brain_health
 24053  GET              /api/channel/categories                          api_channel_categories
 24059  POST             /api/channel/set                                 api_channel_set
 23869  GET              /api/channels/status                             api_channels_status
 22702  POST             /api/chat/send                                   api_chat_send
 14269  GET              /api/chat/send_status                            api_chat_send_status
 10559  GET              /api/checks                                      api_checks
 23374  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23357  GET              /api/clips                                       api_clips
 23390  POST/DELETE      /api/clips/clear                                 api_clips_clear
 22976  GET              /api/cohost                                      api_cohost
 22988  POST             /api/cohost/config                               api_cohost_config
 16008  GET              /api/community/stats                             api_community_stats
 25053  POST             /api/config/restore                              api_config_restore
 25038  GET              /api/config/snapshot                             api_config_snapshot
 15467  GET              /api/cookies/age                                 api_cookies_age
 10626  GET              /api/cookies/health                              api_cookies_health
 10633  POST             /api/cookies/update                              api_cookies_update
 25004  GET              /api/data/export                                 api_data_export
 16523  GET              /api/db/export                                   api_db_export
 16550  POST             /api/db/import                                   api_db_import
 16510  GET              /api/db/summary                                  api_db_summary
 22902  GET              /api/debug/threads                               api_debug_threads
 25939  GET              /api/defense/attacks                             api_defense_attacks
 25906  GET              /api/defense/crowdsec                            api_defense_crowdsec
 25924  GET              /api/defense/fail2ban                            api_defense_fail2ban
 25630  GET              /api/defense/overview                            api_defense_overview
 14630  POST             /api/discord/announce                            api_discord_announce
 14358  GET              /api/discord/clips_week                          api_discord_clips_week
 14574  GET              /api/discord/community                           api_discord_community
 14297  GET              /api/discord/invite                              api_discord_invite
 13760  GET              /api/discord/overview                            api_discord_overview
 13846  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16085  POST             /api/donations/add                               api_donations_add
 16118  GET              /api/donations/manual                            api_donations_manual
 16126  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16021  POST             /api/donations/reset                             api_donations_reset
 16142  GET              /api/donations/summary                           api_donations_summary
 15258  GET              /api/events                                      api_events
 14405  GET              /api/events/stream                               api_events_stream
 17178  GET              /api/evolution/changelog                         api_evolution_changelog
 17163  GET              /api/evolution/history                           api_evolution_history
 17103  GET              /api/evolution/learned                           api_evolution_learned
 17125  GET              /api/evolution/proposals                         api_evolution_proposals
 17146  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17093  POST             /api/evolution/run                               api_evolution_run
 17193  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17058  GET              /api/evolution/status                            api_evolution_status
 16357  GET              /api/finanzamt/entries                           api_finanzamt_entries
 16377  POST             /api/finanzamt/entry                             api_finanzamt_add
 16404  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15271  GET              /api/forecast/storage                            api_forecast_storage
 12292  GET              /api/freeai/status                               api_freeai_status
 13702  GET              /api/health                                      api_health
 15289  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15285  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23025  GET              /api/highlights                                  api_highlights
 23037  POST             /api/highlights/config                           api_highlights_config
 23910  GET              /api/kick/channel                                api_kick_channel
 23931  POST             /api/kick/channel                                api_kick_channel_set
 13429  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13497  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13475  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13414  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13454  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23149  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23218  POST             /api/kickmod/config                              api_kickmod_config
 23263  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23277  GET              /api/kickmod/learned                             api_kickmod_learned
 23304  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23284  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 23615  POST             /api/kickmod/say                                 api_kickmod_say
 23591  POST             /api/kickmod/start                               api_kickmod_start
 23189  GET              /api/kickmod/status                              api_kickmod_status
 23602  POST             /api/kickmod/stop                                api_kickmod_stop
 10411  POST             /api/login                                       dashboard_login_submit
 15993  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12707  POST             /api/marketing/config                            api_marketing_config
 12732  GET              /api/marketing/preview                           api_marketing_preview
 12742  POST             /api/marketing/send-now                          api_marketing_send_now
 12681  GET              /api/marketing/status                            api_marketing_status
 12699  POST             /api/marketing/toggle                            api_marketing_toggle
 23052  GET              /api/moderation/feed                             api_moderation_feed
 13260  POST             /api/news/config                                 api_news_config
 13226  GET              /api/news/creators                               api_news_creators
 13237  POST             /api/news/creators/generate                      api_news_creators_generate
 13302  POST             /api/news/generate-now                           api_news_generate_now
 13297  GET              /api/news/items                                  api_news_items
 13288  GET              /api/news/preview                                api_news_preview
 13207  GET              /api/news/status                                 api_news_status
 13252  POST             /api/news/toggle                                 api_news_toggle
 15850  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14234  GET              /api/notify/status                               api_notify_status
 14245  POST             /api/notify/test                                 api_notify_test
 14220  GET              /api/ops/audit                                   api_ops_audit
 15921  GET              /api/ops/db-stats                                api_ops_db_stats
 15949  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14026  GET              /api/ops/errors                                  api_ops_errors
 15870  GET              /api/ops/healthcheck                             api_ops_healthcheck
 16605  GET              /api/ops/log-tail                                api_ops_log_tail
 12137  GET              /api/ops/logtail                                 api_ops_logtail
 13967  GET              /api/ops/metrics                                 api_ops_metrics
 13950  GET              /api/ops/resource_history                        api_ops_resource_history
 16579  GET              /api/ops/version                                 api_ops_version
 10829  GET              /api/outcomes                                    api_outcomes
 24534  POST             /api/overlay/config                              api_overlay_config
 24521  POST             /api/overlay/event                               api_overlay_event
 24426  GET              /api/overlay/state                               api_overlay_state
 10862  GET              /api/profile/<username>                          api_profile
 15475  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15297  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15423  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15400  GET              /api/proxy/trend                                 api_proxy_trend
 13181  GET              /api/public/stats                                api_public_stats
 10513  GET              /api/pulse                                       api_pulse
 14821  GET              /api/recording-attempts                          api_recording_attempts
 22637  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 22615  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 22656  POST             /api/restream/<int:rid>/start                    api_restream_start
 22923  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24388  GET              /api/restream/chatfeed                           api_restream_chatfeed
 22591  POST             /api/restream/create                             api_restream_create
 13505  GET              /api/restream/deck                               api_restream_deck
 12228  GET              /api/restream/health                             api_restream_health
 24410  POST             /api/restream/layout                             api_restream_layout
 22564  GET              /api/restream/list                               api_restream_list
 12201  POST             /api/restream/report                             api_restream_report
 22936  POST             /api/restream/start_all                          api_restream_start_all
 22962  POST             /api/restream/stop_all                           api_restream_stop_all
 12455  GET              /api/restream/testpush                           api_testpush_status
 12480  POST             /api/restream/testpush                           api_testpush_run
 16258  GET              /api/restream/verify                             api_restream_verify
 14336  GET              /api/retention/preview                           api_retention_preview
 14345  POST             /api/retention/run                               api_retention_run
 25119  POST             /api/schedule/add                                api_schedule_add
 25109  GET              /api/schedule/list                               api_schedule_list
 25144  POST             /api/schedule/remove                             api_schedule_remove
 15174  GET              /api/search                                      api_search
 25677  GET              /api/selftest                                    api_selftest
 22673  GET              /api/shield/stats                                api_shield_stats
 10532  GET              /api/stats                                       api_stats
 15438  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15365  GET              /api/stats/tiktok-status                         api_tiktok_status
 25084  GET              /api/stats/timeline                              api_stats_timeline
 10600  GET              /api/storage                                     api_storage
 10607  POST             /api/storage/cleanup                             api_storage_cleanup
 15351  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12178  GET              /api/stream/timeline                             api_stream_timeline
 13834  GET              /api/stream/transcript                           api_stream_transcript
 24752  GET              /api/streamer/compare                            api_streamer_compare
 24951  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14310  GET              /api/streamer/detail                             api_streamer_detail
 24976  GET              /api/streamer/digest/<username>                  api_streamer_digest
 24856  GET              /api/streamer/dormant                            api_streamer_dormant
 24932  GET              /api/streamer/exists/<username>                  api_streamer_exists
 24811  GET              /api/streamer/journal/<username>                 api_streamer_journal
 24776  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 24836  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13669  GET              /api/streamers/wall                              api_streamers_wall
 10749  GET              /api/summary/preview                             api_summary_preview
 14886  GET              /api/system                                      api_system
 16206  GET              /api/system/check_timing                         api_check_timing
 16491  GET              /api/system/config_drift                         api_config_drift
 13870  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14081  GET              /api/system/preflight                            api_system_preflight
 14207  GET              /api/system/preflight_history                    api_system_preflight_history
 14470  GET              /api/system/resilience                           api_system_resilience
 15209  GET              /api/tags                                        api_tags_list
 10573  GET              /api/top                                         api_top
 12111  GET              /api/trackings                                   api_trackings
 15739  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 15772  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15245  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15458  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 15801  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15231  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 14660  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 14707  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 14736  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 14718  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10766  POST             /api/trackings/bulk                              api_trackings_bulk
 14675  GET              /api/trackings/export                            api_trackings_export
 15213  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15513  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11126  GET              /api/trend-7d                                    api_trend_7d
 23422  GET              /api/tts/<fn>                                    api_tts_file
 12335  POST             /api/tunnel/set                                  api_tunnel_set
 12314  GET              /api/tunnel/status                               api_tunnel_status
 12346  POST             /api/tunnel/test                                 api_tunnel_test
 12327  POST             /api/tunnel/toggle                               api_tunnel_toggle
 16463  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16440  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16422  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 24562  GET              /api/upload_window                               api_upload_window
 10843  GET              /api/userstats                                   api_userstats
 13313  GET              /api/version                                     api_version
 16319  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16340  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16304  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16288  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 29357  GET              /api/youtube/sendrate                            api_youtube_sendrate
 14859  GET              /archive/<int:eid>/download                      archive_download
 14916  GET              /download/<int:recording_id>                     download
 14782  GET              /health                                          health
 22871  GET              /healthz                                         healthz
 10400  GET              /login                                           dashboard_login_page
 10434  GET              /logout                                          dashboard_logout
 10441  GET              /manifest.webmanifest                            pwa_manifest
 13898  GET              /metrics                                         api_prometheus_metrics
 24371  GET              /overlay                                         overlay_page
 10465  GET              /pwa-icon-<variant>.png                          pwa_icon
 10451  GET              /sw.js                                           pwa_service_worker
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
 26382  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 26841  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 26473  /assign_role            Rolle/Gruppe einem Mitglied geben
 26519  /ban                    Mitglied bannen
 27173  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 27097  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27137  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 27122  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 26964  /clips                  Letzte Highlight-Clips eines Users
 26434  /create_category        Kategorie anlegen
 26403  /create_channel         Text-Channel anlegen (optional in Kategorie)
 26462  /create_group           Nutzergruppe (= Rolle) anlegen
 26445  /create_role            Rolle / Nutzergruppe anlegen
 26419  /create_voice           Voice-Channel anlegen
 26755  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 26871  /event                  Community-Event ankündigen (Admin) — mit Countdown
 26914  /events                 Kommende Community-Events anzeigen
 27010  /follow                 Bei Live-Gang eines Streamers gepingt werden
 26994  /help                   Alle Bot-Befehle anzeigen
 26508  /kick                   Mitglied kicken
 26737  /leaderboard            Top-10 der Community nach XP
 26950  /livenow                Welche getrackten User sind gerade live
 26980  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 26811  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 26543  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 26723  /rank                   Dein Level und Rang anzeigen
 26937  /recstatus              Aktuell laufende Aufnahmen
 26484  /remove_role            Rolle/Gruppe entfernen
 26396  /restream_status        Restream-Status
 26495  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 26688  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 26706  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 27036  /stats                  Statistik zu einem getrackten Streamer
 26308  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 27332  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 27229  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 27205  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 26530  /timeout                Mitglied stummschalten (Minuten)
 27108  /topstreamers           Rangliste der Streamer nach Aufnahmen
 26338  /track                  TikTok-User tracken
 26322  /tracklist              Getrackte TikTok-User dieses Servers
 27025  /unfollow               Live-Pings für einen Streamer abbestellen
 26371  /untrack                TikTok-User nicht mehr tracken
 27058  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 27082  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 27816  on_member_join
 27778  on_message
 27419  on_raw_reaction_add
 27851  on_ready
```

## Top-Level-Symbole in bot_v37.py (551 Funktionen, 2 Klassen)

```
  2410-2411   _abo_key
  2431-2449   _abo_probe_dump
 25219-25229  _active_recorder_sync
 19877-19884  _ad_allowlist
 20990-20996  _agent_for
 25231-25249  _ai_calls_total_sync
 20999-21015  _ai_telemetry
 21497-21515  _alert
 27964-28014  _alert_monitor_loop
 28388-28450  _announce_loop
  3352-3355   _anthropic_key
  3362-3364   _anthropic_model
 10203-10206  _arg_int
  2402-2407   _as_dict
 17775-17780  _audio_cfg
 21651-21673  _audio_tap_cmd
 10336-10347  _auth_cookie
 10303-10332  _auth_guard
  1558-1563   _auto_on
 22540-22558  _auto_restream_loop
 29518-29533  _azrael_broadcast_reply
 29418-29440  _azrael_chat_reply
 29401-29415  _azrael_chat_should_reply
 12907-12925  _azrael_creator_take
 29446-29448  _azrael_gate_cfg
 21020-21034  _azrael_live_state
 24270-24284  _azrael_overlay_state
 21380-21434  _azrael_proactive_loop
 20839-20895  _azrael_reaction_to_chats
 29451-29458  _azrael_reply_all_chats
 29388-29398  _azrael_self_names
 29486-29515  _azrael_send_to
 21037-21058  _azrael_system
 28128-28131  _backup_active
 28209-28222  _backup_loop
 19765-19766  _badwords_path
 27929-27938  _brain_growth_loop
 11202-11229  _brain_growth_snapshot
  2338-2358   _brain_hint_delay
 11194-11196  _brain_history_for
  6774-6802   _brain_notify
 11171-11192  _brain_record
 11198-11200  _brain_stream_recent
 14384-14401  _browser_push
  6818-6905   _build_daily_summary
  2841-3021   _build_native_cmd
 18123-18310  _build_restream_cmd
  3065-3098   _build_ytdlp_cmd
 25171-25178  _cached_probe
  5596-5623   _can_stop_tracking
  1738-1760   _capture_set_cookies
 15561-15564  _cfg_get
 15567-15569  _cfg_set
 24014-24049  _channel_set_all
 17373-17376  _chat_connected
 17379-17395  _chat_disconnected
  8800-8811   _chat_is_forum
 17415-17417  _chat_sanitize
 17419-17428  _chat_src_ok
 17358-17370  _chat_stat
 17398-17401  _chat_stats_snapshot
  3627-3638   _check_ai_alive_sync
  3641-3653   _check_ai_models_sync
 25180-25193  _check_redis_alive_sync
 25195-25215  _check_redis_version_sync
 11801-11844  _classify_pool_anonymity
 11847-11864  _classify_pool_anonymity_bg
   754-758    _claude_chat_sync_metered
 10228-10235  _client_ip
 28482-28509  _clip_prune
 28512-28522  _clip_recfile_for
 29038-29044  _clip_should_velocity
 28563-28645  _clip_to_discord
  3525-3534   _close_ai_session
 29562-29577  _cohost_broadcast
 29544-29548  _cohost_cfg
 29603-29615  _cohost_fire_highlight
 29551-29559  _cohost_gate
 29580-29600  _cohost_highlight
 28694-28728  _community_events_loop
 11025-11027  _conv_messages
  7198-7238   _cookie_alarm_loop
  1810-1814   _cookie_autorefresh_info
  1715-1719   _cookie_header
 14434-14466  _cpu_load_snapshot
  3835-3847   _create_index_safe
 12875-12890  _creator_activity
 12931-12954  _creator_dossier_generate
 12893-12904  _creator_facts_line
 25432-25538  _crowdsec_status
 25398-25429  _crowdsec_via_lapi
 25263-25281  _cscli_bin
 25287-25300  _cscli_path
  7091-7116   _daily_summary_loop
 25318-25335  _darf_journal_lesen
 27941-27961  _db_maintenance_loop
  7063-7088   _db_vacuum_loop
 19900-19924  _detect_foreign_ad
  1315-1326   _diag_path_owner
 21286-21330  _director_finalize
 22097-22104  _director_for
 21235-21283  _director_mark
 28932-28967  _disc_automod_check
 28905-28911  _disc_state_get
 28914-28921  _disc_state_set
 25981-25994  _discord_guild_filesize_bytes
 26180-26189  _discord_invite
 28866-28902  _discord_live_thread
 21437-21449  _discord_notify
 26081-26106  _discord_ops_alert
 28764-28862  _discord_post_user
 26245-27926  _discord_run_once
 26119-26177  _discord_start
 28453-28459  _discord_stop
 26002-26004  _discord_upload_limit_label
 25997-25999  _discord_upload_limit_mb
  7119-7193   _disk_alarm_loop
 30831-30880  _disk_autoclean
 30883-30896  _disk_guard_loop
 30823-30828  _disk_pct
 24327-24330  _donations_unknown_count
 17732-17734  _drawtext_chain
 15013-15015  _dump_all_threads
 11726-11790  _enrich_proxies_with_geo
  1955-1999   _ensure_cookie_file_netscape
 26192-26242  _ensure_discord_invite
 28659-28691  _ensure_error_channel
 11969-12006  _ensure_proxy_ready
  8813-8836   _ensure_topic
   637-639    _env_int
   642-644    _env_int_range
 28731-28761  _error_channel_loop
 21481-21494  _event_webhook
 16666-16672  _evo_build_dir
 16675-16682  _evo_version
 16958-17039  _evolution_cycle
 16691-16711  _evolution_llm_note
 17042-17052  _evolution_loop
 16714-16955  _evolution_write_build
  6216-6250   _extract_file_payload
  2087-2089   _extract_urls_from_streamurl_node
 25303-25310  _f2b_sudo_hint
 21517-21519  _faster_whisper_available
 19789-19801  _fetch_ldnoobw_de
 11615-11633  _fetch_proxy_list
 21931-21959  _fetch_tiktok_room_id
   688-691    _ff_cmd
 15684-15697  _ffmpeg_version_str
 17895-17900  _find_chromium
  3058-3062   _find_external_recorder
  2092-2094   _find_stream_urls
 15612-15637  _fire_webhooks
  7974-7983   _fork_safe
   769-778    _freeai_chat_sync_metered
 25353-25395  _geo_lookup_ips
  3514-3523   _get_ai_session
  7808-7848   _get_live_info
  2628-2635   _get_resolve_semaphore
  8162-8527   _handle_single_tracking
 30675-30677  _hb
 30680-30697  _hb_while
 17433-17435  _highlight_cfg
 17438-17467  _highlight_observe
 17903-17908  _htmlov_screenshot_cmd
 21675-21685  _httpx_proxy
 15645-15657  _in_quiet_hours
 31664-31695  _install_fast_eventloop
 10098-10152  _install_fast_json
 15018-15034  _install_faulthandler
 22783-22792  _intel_ensure_schema
 22830-22861  _intel_index_loop
 22804-22814  _intel_index_one
 22795-22801  _intel_semantic
  5585-5594   _is_authorized
  8092-8098   _is_dead
  2077-2079   _is_hevc
 25338-25344  _is_private_ip
  1461-1468   _is_process_running
  6804-6815   _is_quiet_hours
  1123-1132   _is_upload_window
 10187-10200  _json_error_handler
  7021-7051   _kick_broadcaster_id
 12381-12400  _kick_channel_live
  6938-6980   _kick_follower_count
 13392-13405  _kick_oauth_exchange
 13408-13410  _kick_oauth_page
 13351-13355  _kick_redirect_public
 13342-13348  _kick_redirect_source
 13328-13339  _kick_redirect_uri
  6923-6925   _kick_slug
 13358-13389  _kick_user_token
  3884-3887   _kind_from_filename
 15674-15679  _latest_popularity
 19811-19817  _learned_load
 19808-19809  _learned_path
 19819-19827  _learned_save
 22312-22342  _live_react_loop
 22108-22301  _live_react_worker
 20898-20909  _live_transcript_push
 22303-22310  _live_users
 21333-21377  _living_title_loop
 19768-19776  _load_banned_words_file
  1636-1709   _load_cookies_dict
 28134-28206  _local_backup_scan
 10169-10183  _log_5xx
 18318-18330  _looks_like_codec_err
 18313-18315  _looks_like_source_expired
  8055-8085   _loop_fehler
 15038-15047  _loop_heartbeat
 30645-30672  _loop_lag_monitor
 15157-15160  _loop_not_ready
 15050-15118  _loop_watchdog_thread
 20778-20792  _loyalty_add
 20769-20775  _loyalty_get
 20795-20803  _loyalty_top
 16058-16076  _manual_donations_rows
 16079-16081  _manual_donations_total
  8100-8101   _mark_dead
 12548-12577  _marketing_cfg
 12539-12545  _marketing_default_targets
 12534-12536  _marketing_enabled
 12591-12606  _marketing_flavor
 12661-12677  _marketing_loop
 12609-12619  _marketing_post_discord
 12622-12634  _marketing_post_telegram
 12637-12658  _marketing_publish
 12580-12584  _marketing_state_obj
 12587-12588  _marketing_state_save
 29465-29483  _maybe_handle_command
 30982-31006  _maybe_hype_clip
  3802-3825   _migrate_columns
 29740-29751  _mod_is_exempt
 29754-29759  _mod_warn_first
 29762-29765  _mod_warn_text
 17221-17229  _modlog
   890-892    _multistream_targets
  7986-7987   _nc_create_subprocess_exec
  7990-7991   _nc_create_subprocess_shell
 12772-12788  _news_cfg
 12759-12761  _news_enabled
 12826-12867  _news_facts
 12981-13003  _news_generate
 13186-13203  _news_loop
 12764-12769  _news_output_path
 12870-12872  _news_phrase
 12957-12978  _news_phrase_impl
 12801-12808  _news_read
 12791-12794  _news_state_obj
 12797-12798  _news_state_save
 12811-12823  _news_write
 17259-17261  _normalize_ingest
  2269-2286   _note_check_duration
 20924-20932  _oracle_memories
 21190-21224  _oracle_memorize
 20935-20948  _oracle_persona
 20917-20921  _oracle_recent_text
 17558-17566  _ov_atomic_write
 17546-17552  _ov_bar
 19724-19736  _ov_clip_text
 17555-17556  _ov_oneline
 24338-24367  _overlay_push
 17849-17892  _overlay_render_size
 17320-17324  _overlay_session_reset
 24286-24289  _overlay_src_ok
 19887-19897  _own_invites
 16039-16055  _parse_eur
 17844-17846  _parse_size
 25546-25626  _parse_ssh_attacks
  7410-7443   _pause_resume_cmd
  1764-1808   _persist_refreshed_cookies
  1602-1634   _pick_checked_pull_proxy
 10255-10260  _pin_auth_value
 10292-10293  _pin_clear_fail
 10272-10275  _pin_locked
 10278-10289  _pin_note_fail
 10263-10269  _pin_ok
 24176-24178  _piper_available
 24141-24163  _piper_list_voices
 24183-24208  _piper_pick_model
 24220-24267  _piper_say
 24134-24138  _piper_voice_roots
 15574-15609  _post_json_threaded
 17823-17841  _probe_video_size
  1489-1506   _proc_is_recorder
 11713-11724  _proxy_geo_cache_put
 11940-11966  _proxy_pool_refresh_loop
  1568-1599   _proxy_report_recording
 15003-15005  _prune_stall_dumps
 13006-13127  _public_stats
 21452-21478  _push_notify
 10394-10396  _pwa_dir
 11684-11699  _quick_validate_proxy
 15640-15642  _quiet_hours_config
 10359-10392  _rate_guard
 20743-20749  _react_warn
  7894-7933   _reap_proc
  2309-2331   _record_check_outcome
   683-685    _redact_stream_urls
 11867-11937  _refresh_proxy_pool
 24166-24172  _resolve_piper_model
  2103-2193   _resolve_via_html
  2451-2605   _resolve_via_webcast_api_v2
  2668-2730   _resolve_via_ytdlp
 29084-29213  _resolve_youtube_ingest
 22381-22388  _restream_active_platforms
 17305-17316  _restream_active_sources
 21962-22061  _restream_chat_guardian
 17470-17542  _restream_chat_push
 17232-17244  _restream_enabled
 17911-17998  _restream_html_overlay_start
 18001-18014  _restream_html_overlay_stop
  1071-1073   _restream_layout_mode
 17270-17293  _restream_overlay_files
 22346-22378  _restream_platform_state
 22502-22537  _restream_resume_after_restart
 18062-18120  _restream_tts_enqueue_wav
 17785-17817  _restream_tts_feeder
 17782-17783  _restream_tts_fifo_path
 18017-18044  _restream_tts_start
 18046-18060  _restream_tts_stop
 22391-22499  _restream_verify_loop
 28099-28111  _retention_loop
 28058-28096  _retention_scan
  2413-2415   _room_is_abo
  6254-6371   _run_ai_call
 15141-15154  _run_async_from_flask
 25347-25350  _run_priv
 31652-31660  _run_selfcheck_and_exit
 28114-28125  _s3_client
  8103-8149   _safe_send
  4737-4753   _sample_net_throughput
 19778-19786  _save_banned_words_file
  2361-2388   _schedule_next_check
 28017-28055  _scheduler_loop
  3828-3832   _schema_pk
 15162-15167  _scraper_session
 29768-29807  _screen_full
 13718-13755  _sec_headers
  2082-2084   _select_stream_from_data_section
 31465-31649  _selfcheck
  1146-1150   _should_defer_upload
 28525-28560  _shrink_for_discord
 30903-30920  _sign_health_check
 30923-30942  _sign_health_loop
  8003-8014   _spawn
  8017-8047   _spawn_from_flask
 25670-25673  _st_befund
 21687-21928  _start_chat_listener
 15121-15138  _start_loop_watchdog
 13151-13177  _stats_loop
 13130-13133  _stats_output_path
 13136-13148  _stats_write
  8595-8609   _storage_cleanup_loop
 30962-30969  _story_for
  3120-3126   _stream_url_expiry
  3135-3141   _stream_url_is_fresh
  3128-3133   _stream_url_ttl
 19851-19858  _streamer_persona_get
 19833-19839  _streamer_personas_load
 19830-19831  _streamer_personas_path
 19841-19849  _streamer_personas_save
 17737-17741  _studio_chain
 28231-28353  _system_backup
 28356-28384  _system_backup_loop
 11636-11675  _test_proxy
 12422-12431  _testpush_cfg
 12434-12451  _testpush_exec
 12403-12419  _testpush_resolve_live
  8772-8782   _tg_topics_load_into_mem
  8769-8770   _tg_topics_path
  8784-8791   _tg_topics_save
 24880-24928  _tiktok_account_exists
 10238-10246  _token_ok
  8794-8798   _topic_forget
 15660-15671  _tracking_max_duration
  1373-1396   _try_attach_file_handler
 24210-24218  _tts_cleanup
 12307-12310  _tunnel_effective
 23636-23689  _twitch_channel_status
 29810-29952  _twitch_chat_loop
 29626-29727  _twitch_eventsub_loop
 16484-16487  _twitch_oauth_page
  1169-1182   _upload_queue_add
  1193-1195   _upload_queue_count
  1152-1161   _upload_queue_load
  1142-1144   _upload_queue_path
  1184-1191   _upload_queue_remove
  1163-1167   _upload_queue_save
  1197-1235   _upload_window_loop
  7867-7874   _uptime_s
 17247-17256  _url_host
   747-751    _usage_record_claude
  6983-7011   _viewer_sample_loop
  7053-7060   _viewer_stats
 10296-10299  _wants_html
  7877-7891   _warn_empty_env
 30718-30813  _watchdog_loop
 29367-29375  _wchat_thank_ok
 21521-21551  _whisper_get_model
  7964-7971   _whisper_native_section
 20730-20736  _whisper_pool
 21620-21649  _whisper_segments
 21553-21617  _whisper_transcribe
 17568-17730  _write_restream_overlay
 29980-30053  _youtube_api_chat_loop
 23692-23795  _youtube_api_status
 23798-23865  _youtube_channel_status
 30056-30213  _youtube_chat_loop
 29219-29232  _youtube_restream_autoconfig
 29235-29259  _youtube_restream_autoconfig_inner
 29325-29353  _youtube_send
 23970-24011  _youtube_set_channel
 29262-29296  _yt_access_token
 29299-29314  _yt_live_chat_id
 29973-29977  _yt_oauth_configured
 29320-29322  _yt_sendrate_cfg
 29955-29970  _yt_timeout
  2652-2653   _ytdlp_detect_available
  2655-2666   _ytdlp_note_result
 15008-15010  _zombie_child_count
  7744-7768   about
  4003-4007   add_ai_log_entry
  3920-3923   add_archive_entry
  4850-4865   add_archive_rule
  4432-4466   add_recording
  4093-4110   add_tracking
  4527-4544   add_tracking_tag
  6374-6407   ai
  3667-3706   ai_chat
  3740-3750   ai_history_append
  3752-3757   ai_history_clear
  3729-3738   ai_history_load
  3714-3727   ai_rate_limit_check
  6436-6444   aireset
 21061-21080  azrael_chat
 30218-30340  brain_cmd
  3144-3328   build_recording_cmd
  4113-4190   bulk_add_trackings
  7241-7300   bulkadd
  8612-8752   check_all_trackings
  4277-4289   claim_live_transition
 19927-20673  class KickModerator
 18333-19611  class RestreamManager
 12051-12093  classify_proxy_anonymity
  6482-6680   cleanup
  5445-5486   cleanup_old_recordings
  4423-4430   clear_recording
 28970-29035  clip_moment
  4998-5041   cluster_failures
  4681-4730   compute_storage_forecast
  7363-7407   cookies_cmd
  5287-5293   cookies_days_old
  4084-4090   count_trackings_for_chat
  3990-4001   decide_preferred_recorder
  3930-3933   delete_archive_entry
  4867-4875   delete_archive_rule
  5911-6058   diag
 30343-30404  einnahmen_cmd
  4675-4678   find_recordings_by_fingerprint
  3951-3967   finish_recording_attempt
  4222-4232   get_all_active_trackings
  4029-4032   get_all_checks
  4468-4471   get_all_recordings
  4569-4579   get_all_tags_with_counts
  4652-4655   get_annotations_for_recording
  3925-3928   get_archive_entry
  4645-4648   get_bookmarked_recordings
  1831-1948   get_cookie_health
  4518-4524   get_event_log
  3974-3988   get_last_recording_attempt
  2733-2838   get_live_status
  5201-5204   get_manual_recordings
  4660-4663   get_or_compute_inspect_sync
  5521-5565   get_outcome_breakdown
  4626-4634   get_priority_poll_interval
  4828-4837   get_profile_snapshots
  4009-4019   get_recent_ai_log
  3969-3972   get_recent_recording_attempts
  4473-4476   get_recording_by_id
  4638-4641   get_recording_note
  3462-3485   get_redis
  4060-4076   get_stats
  5412-5443   get_storage_stats
  4559-4567   get_tags_for_tracking
  4968-4982   get_tiktok_status_distribution
  4613-4624   get_tracking_priority
  4291-4300   get_tracking_state
  4218-4220   get_trackings_for_group
  5217-5220   get_trash_recordings
  9456-10066  handle_recording_finished
  3850-3875   init_db
  5335-5389   inspect_stream_url
 24333-24335  is_revenue_platform
  4840-4848   list_archive_rules
  5715-5753   live
  8152-8160   live_check_worker
  3537-3571   llm_chat
  3594-3622   llm_chat_sync
  3579-3591   llm_list_models
  4484-4510   log_event
  1423-1456   log_recording_failure
  7557-7606   logs_cmd
 31010-31455  main
  6410-6433   on_ai_media
  7683-7709   on_ai_reply
  7712-7741   on_azrael_mention
  7773-7803   on_callback
 21083-21187  oracle_handle
  7446-7449   pause_tracking
  5575-5580   profile_keyboard
  5296-5332   quick_restart_tracking
  7508-7554   quota
  8529-8592   reaper_loop
  4964-4966   record_tiktok_status
  6449-6479   recstatus
  3487-3495   redis_get_json
  3497-3503   redis_set_json
  4192-4216   remove_tracking
  4546-4557   remove_tracking_tag
 30407-30417  report_cmd
 12096-12098  report_proxy_result
  2196-2223   resolve_tiktok_live_stream
  5212-5215   restore_recording
  7452-7455   resume_tracking
  4878-4958   run_archive_rules
 30420-30625  run_bot
 14930-14977  run_flask
  4756-4801   sample_bandwidth_for_active
  4807-4826   save_profile_snapshot
  4021-4027   save_tiktok_check
  4415-4421   set_recording_file
  4235-4273   set_tracking_paused
  4582-4611   set_tracking_priority
  5207-5210   soft_delete_recording
  8841-9454   split_and_send_video
  5628-5670   start
  3935-3949   start_recording_attempt
  6683-6721   stats
  5182-5199   stop_manual_recording
  7458-7505   stoprec
  6908-6916   summary_cmd
  7609-7680   sysres
  6060-6204   teststream
  5672-5713   tiktok
  7303-7360   topusers
  5790-5847   track
  5755-5787   track_exact
  5861-5909   tracklist
  5048-5180   trigger_manual_recording
  4376-4413   try_acquire_recording_lock
  5223-5282   universal_search
  5849-5859   untrack
  4670-4673   update_recording_fingerprint
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
